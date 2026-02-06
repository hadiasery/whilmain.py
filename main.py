import streamlit as st
import pandas as pd
import yfinance as yf
import time

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="رادار هادي - قناص الحيتان 🐳", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stTable { background-color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 رادار هادي المطوّر (نظام التنبيه الذكي)")
st.write("✅ التنبيه يظهر عند سيولة +500,000$ | اللون الأخضر مخصص لصفقات الحيتان فقط.")

# قائمة الشركات
symbols = ["PLTR", "SOFI", "NIO", "MARA", "TSLA", "AAPL", "NVDA", "RIVN", "AMD"]

if 'market_data' not in st.session_state:
    st.session_state.market_data = {}

table_placeholder = st.empty()

# --- 2. دالة تلوين الصفوف (أخضر عادي عند اكتشاف حوت) ---
def highlight_whales(row):
    # التلوين يعتمد على القيمة الرقمية (التي سنخفيها من العرض)
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
            
            # تحديد نوع التنبيه (Call أو Put) بناءً على السعر الحالي مقارنة بالإغلاق
            # إذا السعر فوق الإغلاق والسيولة ضخمة غالباً Call، والعكس صحيح
            order_type = "CALL 🟢" if price >= prev_close else "PUT 🔴"
            
            # تحديث البيانات
            st.session_state.market_data[symbol] = {
                "الشركة": symbol,
                "السعر الآن": price,
                "السيولة المتدفقة": f"${flow_value:,.0f}",
                "التنبيه": f"🐳 {order_type}" if flow_value >= 500000 else "مراقبة..",
                "السيولة الرقمية": flow_value # هذا العمود سنستخدمه للفرز والتلوين ثم نخفيه
            }
            
            with table_placeholder.container():
                if st.session_state.market_data:
                    df = pd.DataFrame(st.session_state.market_data.values())
                    
                    # الترتيب حسب السعر (الأعلى أولاً)
                    df = df.sort_values(by='السعر الآن', ascending=False)
                    
                    # تحسين شكل السعر للعرض
                    df_display = df.copy()
                    df_display['السعر الآن'] = df_display['السعر الآن'].apply(lambda x: f"${x:.2f}")
                    
                    # إخفاء العمود الأخير (السيولة الرقمية) من العرض فقط
                    display_cols = ["الشركة", "السعر الآن", "السيولة المتدفقة", "التنبيه"]
                    
                    # تطبيق التنسيق على الأعمدة المختارة
                    styled_df = df[display_cols + ["السيولة الرقمية"]].style.apply(highlight_whales, axis=1)
                    
                    # عرض الجدول مع إخفاء العمود الرقمي تقنياً
                    st.table(df_display[display_cols].style.apply(highlight_whales, axis=1))
            
            time.sleep(0.1)
        except:
            continue
