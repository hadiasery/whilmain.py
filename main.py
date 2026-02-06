import streamlit as st
import pandas as pd
import yfinance as yf
import time

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="رادار هادي V61.0 - القناص الصامت", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stTable { background-color: white; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏹 رادار هادي - نظام القنص الصامت")
st.write("⚠️ **الوضع الحالي:** التنبيه (Call/Put) والتلوين الأخضر **معطلان تماماً** ولن يظهرا إلا عند رصد سيولة $\ge$ 50,000,000$.")

# --- 2. الشريط الجانبي ---
with st.sidebar:
    st.header("🛡️ قواعد حماية الـ $50")
    st.info("1. لا تدخل بدون علامة التاج الذهبي 👑")
    st.info("2. اللون الأخضر يعني دخول الحوت الآن")
    api_key = st.text_input("أدخل API KEY", type="password")
    api_secret = st.text_input("أدخل SECRET KEY", type="password")

symbols = ["PLTR", "SOFI", "NIO", "MARA", "TSLA", "AAPL", "NVDA", "RIVN", "AMD", "AMC"]

if 'price_history' not in st.session_state:
    st.session_state.price_history = {}

# --- 3. دالة التلوين الصارمة (50 مليون فقط) ---
def highlight_whales(row, df_original):
    symbol = row['الشركة']
    liquidity = df_original.loc[df_original['الشركة'] == symbol, 'السيولة الرقمية'].values[0]
    # التلوين لا يحدث إلا إذا تجاوزت السيولة 50 مليون
    if liquidity >= 50000000:
        return ['background-color: #2ecc71; color: white; font-weight: bold'] * len(row)
    return [''] * len(row)

# --- 4. محرك التشغيل المستمر ---
if st.button("بدء الرصد اللحظي 🚀"):
    placeholder = st.empty()
    
    while True:
        current_data = []
        for symbol in symbols:
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.fast_info
                
                price = info.last_price
                volume = info.last_volume
                flow_value = price * volume 
                
                # جلب السعر السابق
                old_price = st.session_state.price_history.get(symbol, price)
                st.session_state.price_history[symbol] = price
                
                # --- المنطق الحاسم: التنبيه يكون "انتظار" دائماً إلا في حالة الـ 50 مليون ---
                status = "⚪ عادي"
                signal = "انتظار ⏳"
                
                if flow_value >= 50000000:
                    status = "👑 حوت ذهبي"
                    # لا نحدد النوع إلا داخل هذا الشرط فقط
                    if price > old_price:
                        signal = "CALL 🟢"
                    elif price < old_price:
                        signal = "PUT 🔴"
                    else:
                        signal = "تمركز ⚪"
                
                current_data.append({
                    "الشركة": symbol,
                    "السعر الآن": price,
                    "الحالة": status,
                    "التنبيه": signal,
                    "السيولة الرقمية": flow_value 
                })
            except:
                continue

        # --- 5. العرض ---
        if current_data:
            df_full = pd.DataFrame(current_data)
            df_full = df_full.sort_values(by='السيولة الرقمية', ascending=False)
            
            df_display = df_full[["الشركة", "السعر الآن", "الحالة", "التنبيه"]].copy()
            df_display['السعر الآن'] = df_display['السعر الآن'].apply(lambda x: f"${x:.2f}")
            
            with placeholder.container():
                st.subheader(f"📡 مراقبة السيولة المؤسساتية - {time.strftime('%H:%M:%S')}")
                st.table(df_display.style.apply(lambda row: highlight_whales(row, df_full), axis=1))
        
        time.sleep(2)
else:
    st.info("الرادار متوقف. بانتظار أمر التشغيل...")
