import streamlit as st
import pandas as pd
import yfinance as yf
import time

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="رادار هادي - النسخة النهائية 🐳", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stTable { background-color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 رادار هادي (القناص الذكي)")
st.write("✅ التنبيه: +500,000$ | الترتيب: حسب السعر الأعلى | الحالة: مباشر")

# قائمة الشركات
symbols = ["PLTR", "SOFI", "NIO", "MARA", "TSLA", "AAPL", "NVDA", "RIVN", "AMD"]

if 'market_data' not in st.session_state:
    st.session_state.market_data = {}

table_placeholder = st.empty()

# --- 2. دالة تلوين الصفوف ---
def highlight_whales(row):
    # نستخدم السيولة الرقمية لتحديد التلوين
    if row['السيولة الرقمية'] >= 500000:
        return ['background-color: #2ecc71; color: white; font-weight: bold'] * len(row)
    return [''] * len(row)

# --- 3. حلقة الرصد والتحديث ---
while True:
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.fast_info
            
            price = info.last_price
            prev_close = info.previous_close
            volume = info.last_volume
            flow_value = price * volume 
            
            # تحديد نوع التنبيه
            order_type = "CALL 🟢" if price >= prev_close else "PUT 🔴"
            
            # تحديث البيانات في الذاكرة
            st.session_state.market_data[symbol] = {
                "الشركة": symbol,
                "السعر الآن": price,
                "السيولة المتدفقة": f"${flow_value:,.0f}",
                "التنبيه": f"🐳 {order_type}" if flow_value >= 500000 else "مراقبة..",
                "السيولة الرقمية": flow_value 
            }
        except:
            continue

    # --- 4. عرض الجدول خارج حلقة الـ for لضمان الثبات ---
    with table_placeholder.container():
        if st.session_state.market_data:
            # تحويل البيانات لجدول
            df = pd.DataFrame(st.session_state.market_data.values())
            
            # ترتيب حسب السعر
            df = df.sort_values(by='السعر الآن', ascending=False)
            
            # تجهيز نسخة العرض (بدون عمود السيولة الرقمية)
            df_display = df.copy()
            df_display['السعر الآن'] = df_display['السعر الآن'].apply(lambda x: f"${x:.2f}")
            
            # تطبيق التلوين مع استثناء عمود السيولة الرقمية من العرض النهائي
            final_df = df_display[["الشركة", "السعر الآن", "السيولة المتدفقة", "التنبيه"]]
            
            # تلوين الجدول بناءً على السيولة الرقمية الموجودة في الـ DF الأصلي
            styled_df = df.style.apply(highlight_whales, axis=1)
            
            # عرض الأعمدة المطلوبة فقط للمستخدم
            st.table(df.drop(columns=['السيولة الرقمية']).style.apply(highlight_whales, axis=1))

    time.sleep(2) # تحديث كل ثانيتين لضمان استقرار الجدول
