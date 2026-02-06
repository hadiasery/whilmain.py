import streamlit as st
import pandas as pd
import yfinance as yf
import time

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="رادار هادي - القناص النهائي 🐳", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stTable { background-color: white; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 رادار هادي للقنص (النسخة النهائية)")
st.write("📊 الشركات الصغيرة: تنبيه عند 1M$ | الشركات الكبرى: تنبيه عند 50M$")

# قائمة الشركات (مقسمة لفرص رخيصة وعمالقة)
symbols = ["PLTR", "SOFI", "NIO", "MARA", "TSLA", "AAPL", "NVDA", "RIVN", "AMD", "AMC"]

if 'market_data' not in st.session_state:
    st.session_state.market_data = {}
if 'price_history' not in st.session_state:
    st.session_state.price_history = {}

table_placeholder = st.empty()

# --- 2. دالة التلوين الذكية بناءً على حجم الشركة ---
def highlight_whales(row, df_original):
    symbol = row['الشركة']
    liquidity = df_original.loc[df_original['الشركة'] == symbol, 'السيولة الرقمية'].values[0]
    
    # تحديد سقف التلوين حسب نوع الشركة
    limit = 50000000 if symbol in ["TSLA", "NVDA", "AAPL", "AMD"] else 1000000
    
    if liquidity >= limit:
        return ['background-color: #2ecc71; color: white; font-weight: bold'] * len(row)
    return [''] * len(row)

# --- 3. محرك الرصد ---
while True:
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.fast_info
            price = info.last_price
            volume = info.last_volume
            flow_value = price * volume 
            
            # تحديد السقف (Limit)
            limit = 50000000 if symbol in ["TSLA", "NVDA", "AAPL", "AMD"] else 1000000
            
            # اتجاه السعر
            old_price = st.session_state.price_history.get(symbol, price)
            
            # منطق التنبيه ورصد الحيتان
            if flow_value >= limit:
                whale_detect = "حوت 🐳"
                if price > old_price: signal = "CALL 🟢"
                elif price < old_price: signal = "PUT 🔴"
                else: signal = "تمركز ⚪"
            else:
                whale_detect = "—"
                signal = "انتظار ⏳"
            
            st.session_state.price_history[symbol] = price
            st.session_state.market_data[symbol] = {
                "الشركة": symbol,
                "السعر الآن": price,
                "رصد الحيتان": whale_detect,
                "التنبيه": signal,
                "السيولة الرقمية": flow_value 
            }
        except:
            continue

    # --- 4. العرض النهائي الصافي ---
    with table_placeholder.container():
        if st.session_state.market_data:
            df_full = pd.DataFrame(list(st.session_state.market_data.values()))
            # الترتيب حسب السيولة (الأعلى دائماً في القمة)
            df_full = df_full.sort_values(by='السيولة الرقمية', ascending=False)
            
            # عرض الأعمدة المطلوبة فقط (بدون المال المتدفق)
            cols_to_show = ["الشركة", "السعر الآن", "رصد الحيتان", "التنبيه"]
            df_display = df_full[cols_to_show].copy()
            df_display['السعر الآن'] = df_display['السعر الآن'].apply(lambda x: f"${x:.2f}")
            
            st.table(df_display.style.apply(lambda row: highlight_whales(row, df_full), axis=1))

    time.sleep(2)
