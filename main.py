import streamlit as st
import pandas as pd
import requests
import datetime
import time

# --- 1. إعدادات الواجهة ---
st.set_page_config(page_title="رادار هادي لصيد الحيتان", layout="wide")
st.title("🐳 رادار هادي: صيد صفقات الحيتان (رصد فقط)")

# --- 2. إدارة البيانات (في الخفاء) ---
# سنستخدم مفتاح تجريبي للبيانات (يمكنك استبداله بمفتاحك الخاص لاحقاً)
POLYGON_API_KEY = "YOUR_FREE_API_KEY" 

if 'whale_log' not in st.session_state:
    st.session_state.whale_log = []

# --- 3. وظيفة الرصد (Whale Detection Logic) ---
def fetch_whale_trades(symbol):
    """جلب الصفقات الضخمة من السوق الأمريكي"""
    url = f"https://api.polygon.io/v3/trades/{symbol}?limit=10&apiKey={POLYGON_API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            trades = response.json().get('results', [])
            for t in trades:
                # حساب قيمة الصفقة: السعر × الكمية
                trade_value = t['p'] * t['s']
                
                # إذا كانت الصفقة أكبر من حد الحوت المحدد
                if trade_value >= whale_limit:
                    new_entry = {
                        "الوقت": datetime.datetime.now().strftime("%H:%M:%S"),
                        "السهم": symbol,
                        "السعر": f"${t['p']:,.2f}",
                        "الكمية": f"{t['s']:,}",
                        "القيمة الكلية": f"${trade_value:,.0f} 🚨"
                    }
                    # منع التكرار وإضافة الصيد الجديد في الأعلى
                    if not st.session_state.whale_log or st.session_state.whale_log[0]['القيمة الكلية'] != new_entry['القيمة الكلية']:
                        st.session_state.whale_log.insert(0, new_entry)
                        st.session_state.whale_log = st.session_state.whale_log[:20]
    except Exception as e:
        pass

# --- 4. واجهة التحكم ---
st.sidebar.header("⚙️ إعدادات الرادار")
whale_limit = st.sidebar.number_input("حد صفقة الحوت ($)", value=100000, step=50000)
symbols_to_track = st.sidebar.text_input("الأسهم المراقبة", "TSLA,NVDA,AAPL,SPY").split(',')

# --- 5. العرض المباشر ---
st.subheader("📊 الصيد اللحظي (مراقبة فقط)")

if st.sidebar.button("تشغيل الرادار 🚀"):
    st.sidebar.success("الرادار يعمل الآن في الخفاء...")
    
    placeholder = st.empty()
    
    while True:
        for sym in symbols_to_track:
            fetch_whale_trades(sym.strip().upper())
        
        with placeholder.container():
            if st.session_state.whale_log:
                df = pd.DataFrame(st.session_state.whale_log)
                st.table(df) # عرض الصيد في جدول منظم
            else:
                st.info("🌊 المسح جارٍ.. بانتظار ظهور أول حوت في المحيط.")
        
        time.sleep(10) # تحديث كل 10 ثوانٍ لضمان استقرار السيرفر
