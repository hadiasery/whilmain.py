import streamlit as st
import requests
import pandas as pd
import random

# قائمة بروكسيات (هذه أمثلة، في الواقع نستخدم ملقمات حية)
def get_proxy():
    # في النسخة الاحترافية، نستخدم API لجلب بروكسي جديد كل ثانية
    proxies = [
        None, # الطلب العادي
        # "http://username:password@proxy_host:port", # إذا كان لديك بروكسي مدفوع
    ]
    return random.choice(proxies)

def fetch_with_new_ip(ticker):
    url = f"https://query1.finance.yahoo.com/v7/finance/options/{ticker}"
    
    # تغيير الـ User-Agent (تغيير الهوية الرقمية)
    headers = {
        "User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) Firefox/121.0"
        ])
    }

    try:
        # هنا نحاول تغيير الـ IP عبر البروكسي
        proxy = get_proxy()
        response = requests.get(url, headers=headers, proxies={"http": proxy, "https": proxy} if proxy else None, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return data['optionChain']['result'][0]['options'][0]['calls']
        else:
            return f"Error: {response.status_code} (IP Blocked)"
    except Exception as e:
        return str(e)

st.title("🛡️ رادار تغيير الـ IP التلقائي")

ticker = st.text_input("أدخل الرمز لكسر الحظر:", "NVDA")

if st.button('فحص بـ IP جديد 🔄'):
    result = fetch_with_new_ip(ticker)
    
    if isinstance(result, list):
        df = pd.DataFrame(result)
        st.success(f"✅ تم تجاوز الحظر لسهم {ticker}!")
        st.dataframe(df[['strike', 'lastPrice', 'volume', 'openInterest']].sort_values(by='volume', ascending=False).head(10))
    else:
        st.error(f"❌ لا يزال الـ IP محظوراً: {result}")
        st.info("نصيحة: تغيير الـ IP في Streamlit صعب جداً. أفضل وسيلة هي تشغيل الكود من كمبيوترك الشخصي واستخدام VPN.")
