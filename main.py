import streamlit as st
import pandas as pd
import yfinance as yf
import time

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="رادار هادي - القناص 🐳", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stTable { background-color: white; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 رادار هادي (صائد المسابح المظلمة)")
st.write("📊 ترتيب تلقائي حسب السيولة | أخضر = حوت (+500k$)")

symbols = ["PLTR", "SOFI", "NIO", "MARA", "TSLA", "AAPL", "NVDA", "RIVN", "AMD", "AMC"]

# تهيئة الذاكرة المؤقتة
if 'market_data' not in st.session_state:
    st.session_state.market_data = {}
if 'price_history' not in st.session_state:
    st.session_state.price_history = {}

table_placeholder = st.empty()

# --- 2. دالة التلوين الآمنة ---
def highlight_whales(row):
    # نستخدم get لتجنب KeyError في حال فقدان العمود
    liquidity = row.get('السيولة الرقمية', 0)
    if isinstance(liquidity, (int, float)) and liquidity >= 500000:
        return ['background-color: #2ecc71; color: white; font-weight: bold'] * len(row)
    return [''] * len(row)

# --- 3. محرك الرصد اللحظي ---
while True:
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.fast_info
            price = info.last_price
            volume = info.last_volume
            flow_value = price * volume 
            
            # تحديد الاتجاه (CALL/PUT/WAIT)
            old_price = st.session_state.price_history.get(symbol, price)
            if flow_value >= 500000:
                if price > old_price: signal = "🐳 CALL 🟢"
                elif price < old_price: signal = "🐳 PUT 🔴"
                else: signal = "🐳 WHALE ⚪"
            else:
                signal = "⏳ WAIT"
            
            st.session_state.price_history[symbol] = price
            
            # تخزين البيانات في قاموس لضمان سهولة التحويل لـ DataFrame
            st.session_state.market_data[symbol] = {
                "الشركة": symbol,
                "السعر الآن": price,
                "المال المتدفق": f"${flow_value:,.0f}",
                "التنبيه": signal,
                "السيولة الرقمية": flow_value 
            }
        except:
            continue

    # --- 4. العرض الآمن للجدول ---
    with table_placeholder.container():
        if st.session_state.market_data:
            # تحويل البيانات إلى DataFrame
            df = pd.DataFrame(list(st.session_state.market_data.values()))
            
            # التأكد من أن العمود المطلوب للترتيب موجود
            if 'السيولة الرقمية' in df.columns:
                df = df.sort_values(by='السيولة الرقمية', ascending=False)
                
                # تنسيق السعر للعرض
                df_display = df.copy()
                df_display['السعر الآن'] = df_display['السعر الآن'].apply(lambda x: f"${x:.2f}")
                
                # إخفاء العمود الرقمي برمجياً وعرض الباقي
                # نستخدم hide من pandas styler بدلاً من drop لتجنب KeyError
                cols_to_show = ["الشركة", "السعر الآن", "المال المتدفق", "التنبيه"]
                
                st.table(
                    df_display.style.apply(highlight_whales, axis=1)
                    .hide(axis="columns", subset=["السيولة الرقمية"])
                )

    time.sleep(2)
