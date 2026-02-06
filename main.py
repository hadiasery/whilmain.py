import streamlit as st
import pandas as pd
import requests
import datetime
import time

# --- 1. إعدادات الواجهة ---
st.set_page_config(page_title="رادار هادي اللحظي ⚡", layout="wide")
st.title("🎯 رادار هادي: صيد الحيتان اللحظي (أسهم تحت 50$)")
st.write("🚀 الرادار يعمل الآن ببيانات لحظية بالثانية عبر Alpaca API")

# --- 2. المفاتيح الخاصة بك (تم دمجها بنجاح) ---
ALPACA_API_KEY = "CK5KQVW7ZADWQEAJRTJ7LXJPVI"
ALPACA_SECRET_KEY = "6h9om7wsmAAQgqW2ewCWWVFAuTqxjaKmcha2cjjxSMdx"

# قائمة الأسهم الاقتصادية القوية (تحت 50$)
symbols = ["PLTR", "SOFI", "NIO", "F", "LCID", "CCL", "T", "AAL", "MARA"]

if 'whale_history' not in st.session_state:
    st.session_state.whale_history = []

# --- 3. وظيفة جلب البيانات اللحظية ---
def get_live_data():
    for symbol in symbols:
        # رابط جلب آخر صفقة لحظية من Alpaca
        url = f"https://data.alpaca.markets/v2/stocks/{symbol}/trades/latest"
        headers = {
            "APCA-API-KEY-ID": ALPACA_API_KEY,
            "APCA-API-SECRET-KEY": ALPACA_SECRET_KEY
        }
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json().get('trade', {})
                price = data.get('p', 0) # السعر اللحظي
                size = data.get('s', 0)  # حجم الصفقة
                value = price * size     # قيمة الصفقة بالدولار
                
                # فلتر هادي: السعر متاح (تحت 50$) والصفقة كبيرة (فوق 10,000$ كبداية)
                if 0 < price <= 50 and value >= 10000:
                    new_trade = {
                        "الوقت": datetime.datetime.now().strftime("%H:%M:%S"),
                        "السهم": symbol,
                        "السعر اللحظي": f"${price:.2f}",
                        "قيمة الصفقة": f"${value:,.0f} 🐳",
                        "التوصية": "فرصة دخول ⚡"
                    }
                    
                    # منع التكرار وإضافة الصفقة الجديدة في الأعلى
                    if not st.session_state.whale_history or st.session_state.whale_history[0]['قيمة الصفقة'] != new_trade['قيمة صفقة الحوت']:
                        st.session_state.whale_history.insert(0, new_trade)
                        st.session_state.whale_history = st.session_state.whale_history[:15]
            
            # سرعة التحديث (نصف ثانية بين كل سهم) للحصول على أداء سريع جداً
            time.sleep(0.5) 
        except:
            continue

# --- 4. العرض المستمر ---
placeholder = st.empty()

while True:
    get_live_data()
    with placeholder.container():
        if st.session_state.whale_history:
            df = pd.DataFrame(st.session_state.whale_history)
            st.table(df)
        else:
            st.info("الرادار يمسح السوق الآن بالثانية.. بانتظار دخول حوت في الأسهم الاقتصادية 🌊")
    
    st.rerun()
