import streamlit as st
import requests
import pandas as pd
import random
from bs4 import BeautifulSoup

# دالة لجلب قائمة بروكسيات حية لتغيير الـ IP
def get_free_proxies():
    url = 'https://free-proxy-list.net/'
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        proxies = []
        for row in soup.find('table', {'class': 'table'}).find_all('tr')[1:]:
            tds = row.find_all('td')
            try:
                if tds[4].text == 'elite proxy' or tds[4].text == 'anonymous':
                    ip = tds[0].text
                    port = tds[1].text
                    proxies.append(f"http://{ip}:{port}")
            except:
                continue
        return proxies
    except:
        return []

def fetch_data_with_proxy(ticker, proxy_list):
    url = f"https://query1.finance.yahoo.com/v7/finance/options/{ticker}"
    
    # اختيار بروكسي عشوائي لتغيير الـ IP
    proxy = random.choice(proxy_list) if proxy_list else None
    proxies = {"http": proxy, "https": proxy} if proxy else None
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, proxies=proxies, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data['optionChain']['result'][0]['options'][0]['calls'], proxy
        else:
            return f"Blocked (Status: {response.status_code})", proxy
    except:
        return "Connection Failed", proxy

st.title("🛡️ رادار الحيتان - نظام تغيير الـ IP")

if 'proxies' not in st.session_state:
    st.session_state.proxies = get_free_proxies()

st.write(f"🌐 لدينا حالياً {len(st.session_state.proxies)} عنوان IP جاهز للاستخدام.")

ticker = st.text_input("أدخل الرمز (مثلاً NVDA):", "NVDA")

if st.button('تغيير الـ IP والفحص الآن 🔄'):
    with st.spinner('جاري تبديل الـ IP والتسلل...'):
        result, used_ip = fetch_data_with_proxy(ticker, st.session_state.proxies)
        
        if isinstance(result, list):
            st.success(f"✅ نجح الاختراق باستخدام IP: {used_ip}")
            df = pd.DataFrame(result)
            st.dataframe(df[['strike', 'lastPrice', 'volume', 'openInterest']].sort_values(by='volume', ascending=False).head(10))
        else:
            st.error(f"❌ فشل الـ IP ({used_ip}): {result}")
            if st.button('تحديث قائمة الـ IPs'):
                st.session_state.proxies = get_free_proxies()
                st.rerun()
