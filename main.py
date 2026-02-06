import streamlit as st
import pandas as pd
import yfinance as yf
import time

# --- 1. إعدادات الصفحة والنمط ---
st.set_page_config(page_title="رادار هادي - صائد السيولة 🐳", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stTable { background-color: white; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 رادار هادي: مراقبة صفقات المؤسسات والمسابح المظلمة")
st.write("📈 التنبيه: **CALL** (دخول سيولة شرائية) | **PUT** (تسييل بيعي) | **WAIT** (هدوء أو انتظار)")

# الشركات المختارة
symbols = ["PLTR", "SOFI", "NIO", "MARA", "TSLA", "AAPL", "NVDA", "RIVN", "AMD", "AMC"]

if 'market_data' not in st.session_state:
    st.session_state.market_data = {}
if 'price_history' not in st.session_state:
    st.session_state.price_history = {}

table_placeholder = st.empty()

# --- 2. دالة التلوين الذكي ---
def highlight_whales(row):
    # تلوين الصف بالأخضر العادي فقط عند رصد سيولة حوت (نصف مليون فأكثر)
    if row['السيولة الرقمية'] >= 500000:
        return ['background-color: #2ecc71; color: white; font-weight: bold'] * len(row)
    return [''] * len(row)

# --- 3. محرك تحليل التدفق ---
while True:
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.fast_info
            price = info.last_price
            volume = info.last_volume
            flow_value = price * volume 
            
            # --- منطق التنبيه الثلاثي ---
            old_price = st.session_state.price_history.get(symbol, price)
            
            if flow_value >= 500000:
                # إذا كانت السيولة ضخمة، نحدد الاتجاه
                if price > old_price:
                    signal = "🐳 CALL (دخول حوت)"
                elif price < old_price:
                    signal = "🐳 PUT (خروج حوت)"
                else:
                    signal = "🐳 WHALE (تمركز)"
            else:
                # إذا كانت السيولة عادية، نضع حالة الانتظار
                signal = "⏳ WAIT (انتظار)"
            
            # تحديث السعر للتحليل القادم
            st.session_state.price_history[symbol] = price
            
            # تخزين البيانات
            st.session_state.market_data[symbol] = {
                "الشركة": symbol,
                "السعر الآن": f"${price:.2f}",
                "المال المتدفق": f"${flow_value:,.0f}",
                "التنبيه": signal,
                "السيولة الرقمية": flow_value 
            }
        except:
            continue

    # --- 4. العرض والترتيب ---
    with table_placeholder.container():
        if st.session_state.market_data:
            df = pd.DataFrame(st.session_state.market_data.values())
            
            # الترتيب حسب المال المتدفق (الأعلى أولاً) لرؤية المسابح المظلمة في القمة
            df = df.sort_values(by='السيولة الرقمية', ascending=False)
            
            # تحديد الأعمدة للعرض فقط
            display_cols = ["الشركة", "السعر الآن", "المال المتدفق", "التنبيه"]
            
            # عرض الجدول مع تطبيق التلوين وإخفاء عمود الحسابات الرقمية
            st.table(df[display_cols + ["السيولة الرقمية"]].style.apply(highlight_whales, axis=1).set_properties(subset=["السيولة الرقمية"], **{'display': 'none'}))

    time.sleep(2)
