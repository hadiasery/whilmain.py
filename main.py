import streamlit as st
import cloudscraper
import pandas as pd
import io

def bypass_and_scrip():
    # استخدام scraper متطور يتجاوز Cloudflare والحظر
    scraper = cloudscraper.create_scraper() 
    
    # سنحاول سحب بيانات الأوبشن النشطة من مصدر بديل وسريع (مثل Yahoo عبر رابط مختلف)
    url = "https://query1.finance.yahoo.com/v7/finance/options/TSLA" # تجربة على تسلا
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    }

    try:
        response = scraper.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            calls = data['optionChain']['result'][0]['options'][0]['calls']
            df = pd.DataFrame(calls)
            return df
        else:
            return f"Error Code: {response.status_code}"
    except Exception as e:
        return str(e)

st.title("🕵️ رادار الحيتان - كاسر الحظر")

if st.button('اقتناص الفرص الآن ⚡'):
    res = bypass_and_scrip()
    if isinstance(res, pd.DataFrame):
        st.success("✅ نجح الاختراق! إليك عقود تسلا النشطة الآن:")
        # ترتيب حسب الحجم لرؤية الحيتان
        st.dataframe(res[['strike', 'lastPrice', 'volume', 'openInterest']].sort_values(by='volume', ascending=False).head(10))
    else:
        st.error(f"⚠️ لا يزال الجدار قوياً: {res}")
        st.info("💡 الحل النهائي: ياهو حظرت Streamlit تماماً. سأعطيك كوداً يعمل بنظام 'Google Finance' البديل.")
