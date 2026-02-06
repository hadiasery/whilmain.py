import streamlit as st
import pandas as pd
import requests
import datetime
import time

# --- 1. إعدادات الواجهة ---
st.set_page_config(page_title="رادار هادي - البث المباشر ⚡", layout="wide")
st.title("🎯 رادار هادي: صيد الحيتان (مباشر الآن)")

# --- 2. مفاتيحك التي أرسلتها ---
ALPACA_API_KEY = "CK5KQVW7ZADWQEAJRTJ7LXJPVI"
ALPACA_SECRET_KEY = "6h9om7wsmAAQgqW2ewCWWVFAuTqxjaKmcha2cjjxSMdx"

# قائمة أسهم نشطة جداً الآن (للتأكد من الحركة)
symbols = ["TSLA", "NVDA", "AAPL", "PLTR", "SOFI", "MARA", "NIO", "AMD"]

if 'whale_history' not in st.session_state:
    st.session_state.whale_history = []

# --- 3. وظيفة جلب البيانات باستخدام الرابط المباشر ---
def get_live_trades():
    # نستخدم V2 لضمان استلام أحدث الصفقات
    headers = {
        "APCA-API-KEY-ID": ALPACA_API_KEY,
        "APCA-API-SECRET-KEY": ALPACA_SECRET_KEY
    }
    
    for symbol in symbols:
        url = f"https://data.alpaca.markets/v2/stocks/{symbol}/trades/latest"
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                trade = response.json().get('trade', {})
                price = trade.get('p', 0)
                size = trade.get('s', 0)
                value = price * size
                
                # الفلتر: السعر تحت 50$ (لميزانيتك) والقيمة فوق 5,000$ (لتسريع الظهور)
                if 0 < price <= 50 and value >= 5000:
                    new_entry = {
                        "الوقت": datetime.datetime.now().strftime("%H:%M:%S"),
                        "السهم": symbol,
                        "السعر": f"${price:.2f}",
                        "قيمة الصفقة": f"${value:,.0f} 🐳",
                        "ميزانية 50$": "مناسب ✅"
                    }
                    
                    # إضافة الصفقة ومنع التكرار
                    if not st.session_state.whale_history or st.session_state.whale_history[0]['قيمة الصفقة'] != new_entry['قيمة الصفقة']:
                        st.session_state.whale_history.insert(0, new_entry)
                        st.session_state.whale_history = st.session_state.whale_history[:15]
            
            elif response.status_code == 403:
                st.error("❌ المفاتيح غير مفعلة للبيانات اللحظية. تأكد أنك في وضع Paper Trading.")
                return
        except:
            continue

# --- 4. التحديث التلقائي الشامل ---
placeholder = st.empty()

while True:
    get_live_trades()
    with placeholder.container():
        if st.session_state.whale_history:
            st.table(pd.DataFrame(st.session_state.whale_history))
        else:
            st.info(f"الرادار يراقب {symbols} الآن.. بانتظار صفقة حوت بالثانية.")
    
    time.sleep(1) # تحديث كل ثانية
    st.rerun()
