import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
import time

# --- 1. إعدادات الواجهة ---
st.set_page_config(page_title="رادار هادي - الصياد الحر 🦅", layout="wide")
st.title("🎯 رادار هادي: صيد الحيتان (نظام ياهو المباشر)")
st.write("✅ هذا النظام يعمل مباشرة بدون مفاتيح API لتجنب أي تعليق.")

# قائمة الأسهم الأكثر حركة الآن (تحت 50$)
symbols = ["PLTR", "SOFI", "NIO", "F", "LCID", "CCL", "MARA", "RIVN", "SNAP", "SQ"]

if 'whale_history' not in st.session_state:
    st.session_state.whale_history = []

# --- 2. وظيفة جلب البيانات من Yahoo Finance ---
def get_whale_action():
    for symbol in symbols:
        try:
            # جلب بيانات السهم اللحظية
            ticker = yf.Ticker(symbol)
            data = ticker.fast_info
            
            price = data.last_price
            volume = data.last_volume
            # حساب القيمة التقديرية لآخر حركة تداول كبيرة
            value = price * (volume / 100) # تقدير تقريبي لتدفق السيولة
            
            # فلتر هادي (تحت 50$ وحركة نشطة)
            if 0 < price <= 50:
                new_entry = {
                    "الوقت": datetime.datetime.now().strftime("%H:%M:%S"),
                    "السهم": symbol,
                    "السعر الآن": f"${price:.2f}",
                    "قوة السيولة": f"{volume:,.0f} سهم",
                    "الحالة": "مراقبة لحظية 🔥"
                }
                
                # إضافة للجدول
                st.session_state.whale_history.insert(0, new_entry)
                # الاحتفاظ بآخر 15 حركة فقط
                st.session_state.whale_history = st.session_state.whale_history[:15]
        except:
            continue

# --- 3. عرض النتائج وتحديث تلقائي ---
placeholder = st.empty()

while True:
    get_whale_action()
    with placeholder.container():
        if st.session_state.whale_history:
            df = pd.DataFrame(st.session_state.whale_history)
            st.table(df)
        else:
            st.info("جاري سحب البيانات من محرك ياهو.. انتظر ثواني.")
    
    time.sleep(2) # تحديث كل ثانيتين لضمان استقرار الاتصال
    st.rerun()
