import streamlit as st
import pandas as pd
import yfinance as yf
import time

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="رادار هادي - القناص 🐳", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stTable { background-color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 رادار هادي (تنبيه الحيتان اللحظي)")
st.write("✅ التنبيه: +500,000$ | اللون الأخضر: صفقات حيتان | الترتيب: الأعلى سعراً")

# قائمة الشركات
symbols = ["PLTR", "SOFI", "NIO", "MARA", "TSLA", "AAPL", "NVDA", "RIVN", "AMD"]

if 'market_data' not in st.session_state:
    st.session_state.market_data = {}

table_placeholder = st.empty()

# --- 2. دالة تلوين الصفوف (معدلة لتجنب الخطأ) ---
def highlight_whales(row):
    # نتحقق من وجود القيمة أولاً لتجنب KeyError
    liquidity = row.get('السيولة الرقمية', 0)
    if liquidity >= 500000:
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

    # --- 4. عرض الجدول بطريقة آمنة ---
    with table_placeholder.container():
        if st.session_state.market_data:
            # تحويل البيانات لجدول وترتيبها
            df = pd.DataFrame(st.session_state.market_data.values())
            df = df.sort_values(by='السعر الآن', ascending=False)
            
            # تحسين شكل السعر للعرض
            df['السعر الآن'] = df['السعر الآن'].apply(lambda x: f"${x:.2f}")
            
            # نطبق التلوين على كل الجدول أولاً
            styled_df = df.style.apply(highlight_whales, axis=1)
            
            # هنا السر: نحدد فقط الأعمدة التي نريد عرضها للمستخدم
            # السيولة الرقمية ستبقى في الخلفية لعملية التلوين لكن لن تظهر في الجدول
            cols_to_show = ["الشركة", "السعر الآن", "السيولة المتدفقة", "التنبيه"]
            
            st.table(styled_df.set_properties(subset=["السيولة الرقمية"], **{'display': 'none'}).hide(axis="columns", subset=["السيولة الرقمية"]))

    time.sleep(2)
