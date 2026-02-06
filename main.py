import streamlit as st
import pandas as pd
import yfinance as yf
import time

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="رادار هادي للصيد الثمين V61.0", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stTable { background-color: white; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏹 رادار هادي - البث المباشر المستمر")
st.write("📡 الرادار يعمل الآن آلياً ويراقب صفقات الـ **50,000,000$** لحظة بلحظة.")

# --- 2. الشريط الجانبي (API والقواعد) ---
with st.sidebar:
    st.header("🛡️ قواعد حماية الـ $50")
    st.info("1. لا تدخل بدون علامة التاج الذهبي 👑")
    st.info("2. الربح البسيط (5$-10$) هو فوز عظيم")
    st.warning("3. تلوين الصف بالأخضر = حوت الـ 50 مليون")
    st.write("---")
    api_key = st.text_input("أدخل API KEY", type="password")
    api_secret = st.text_input("أدخل SECRET KEY", type="password")

# الشركات المختارة
symbols = ["PLTR", "SOFI", "NIO", "MARA", "TSLA", "AAPL", "NVDA", "RIVN", "AMD", "AMC"]

# تهيئة الذاكرة
if 'price_history' not in st.session_state:
    st.session_state.price_history = {}

# --- 3. دالة التلوين (50 مليون) ---
def highlight_whales(row, df_original):
    symbol = row['الشركة']
    liquidity = df_original.loc[df_original['الشركة'] == symbol, 'السيولة الرقمية'].values[0]
    if liquidity >= 50000000:
        return ['background-color: #2ecc71; color: white; font-weight: bold'] * len(row)
    return [''] * len(row)

# --- 4. محرك التشغيل المستمر ---
if st.button("بدء الرصد اللحظي 🚀"):
    # إنشاء حاوية فارغة للتحديث المستمر دون إعادة تحميل الصفحة
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
                
                # منطق الاتجاه
                old_price = st.session_state.price_history.get(symbol, price)
                st.session_state.price_history[symbol] = price
                
                # فلتر الـ 50 مليون
                if flow_value >= 50000000:
                    status = "👑 حوت ذهبي"
                    if price > old_price: signal = "CALL 🟢"
                    elif price < old_price: signal = "PUT 🔴"
                    else: signal = "تمركز ⚪"
                else:
                    status = "⚪ عادي"
                    signal = "انتظار ⏳"
                
                current_data.append({
                    "الشركة": symbol,
                    "السعر الآن": price,
                    "الحالة": status,
                    "التنبيه": signal,
                    "السيولة الرقمية": flow_value 
                })
            except:
                continue

        # --- 5. تحديث الواجهة برمجياً ---
        if current_data:
            df_full = pd.DataFrame(current_data)
            df_full = df_full.sort_values(by='السيولة الرقمية', ascending=False)
            
            # تجهيز العرض
            display_cols = ["الشركة", "السعر الآن", "الحالة", "التنبيه"]
            df_display = df_full[display_cols].copy()
            df_display['السعر الآن'] = df_display['السعر الآن'].apply(lambda x: f"${x:.2f}")
            
            with placeholder.container():
                st.subheader(f"📡 مسح حي - آخر تحديث: {time.strftime('%H:%M:%S')}")
                st.table(df_display.style.apply(lambda row: highlight_whales(row, df_full), axis=1))
        
        # التوقف لمدة ثانيتين قبل التحديث القادم لضمان الاستمرارية
        time.sleep(2)
else:
    st.info("الرادار متوقف. اضغط على الزر أعلاه ليبدأ العمل المستمر.")
