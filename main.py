import pandas as pd
import requests
import streamlit as st

def nasdaq_whale_hacker(ticker):
    # رابط مباشر يحاكي طلبات متصفح ناسداك الرسمي
    url = f"https://api.nasdaq.com/api/quote/{ticker}/option-chain?assetclass=stocks&limit=20"
    
    # هوية متصفح قوية جداً
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://www.nasdaq.com",
        "Referer": "https://www.nasdaq.com/"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        
        # استخراج مصفوفة العقود
        rows = data['data']['table']['rows']
        df = pd.DataFrame(rows)
        
        # تنظيف البيانات (تحويل النصوص إلى أرقام)
        df['volume'] = pd.to_numeric(df['volume'].str.replace(',', ''), errors='coerce')
        
        # فلتر الحيتان: حجم تداول عالي
        whales = df[df['volume'] > 100].sort_values(by='volume', ascending=False)
        
        return whales[['expiryDate', 'callPut', 'strike', 'lastPrice', 'volume']]
    except Exception as e:
        return None

st.title("🕵️ رادار الحيتان (نسخة ناسداك غير القابلة للحظر)")

if st.button('استرِق السمع الآن 🚀'):
    for t in ["TSLA", "NVDA", "AAPL"]:
        res = nasdaq_whale_hacker(t)
        if res is not None and not res.empty:
            st.success(f"✅ تم صيد بيانات {t} مباشرة من البورصة!")
            st.table(res.head(5))
        else:
            st.error(f"❌ {t}: البورصة لم تستجب، قد يكون السوق مغلقاً أو الرابط تغير.")
