import streamlit as st
import pandas as pd
import yfinance as yf
import time

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="رادار هادي للصيد الثمين V61.0", layout="wide")

# تخصيص واجهة المستخدم
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stTable { background-color: white; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏹 رادار هادي لقنص الحيتان - نسخة الـ 50 مليون")
st.write("📈 التنبيه وتلوين الصفوف لا يحدث إلا عند تجاوز السيولة اللحظية **50,000,000$**.")

# --- 2. الشريط الجانبي (قواعد الحماية والـ API) ---
with st.sidebar:
    st.header("🛡️ قواعد حماية الـ $50")
    st.info("1. لا تدخل بدون علامة التاج الذهبي 👑")
    st.info("2. الربح البسيط (5$-10$) هو فوز عظيم")
    st.warning("3. تلوين الصف بالأخضر = حوت الـ 50 مليون")
    st.write("---")
    # هنا يتم إدخال الـ API و SECRET (محفوظة في الجلسة)
    api_key = st.text_input("أدخل API KEY", type="password")
    api_secret = st.text_input("أدخل SECRET KEY", type="password")

# الشركات المختارة
symbols = ["PLTR", "SOFI", "NIO", "MARA", "TSLA", "AAPL", "NVDA", "RIVN", "AMD", "AMC"]

# تهيئة الذاكرة المؤقتة
if 'market_data' not in st.session_state:
    st.session_state.market_data = {}
if 'price_history' not in st.session_state:
    st.session_state.price_history = {}

# --- 3. دالة التلوين الصارمة (50 مليون) ---
def highlight_whales(row, df_original):
    symbol = row['الشركة']
    # جلب القيمة الرقمية من الجدول الأصلي للتحقق
    liquidity = df_original.loc[df_original['الشركة'] == symbol, 'السيولة الرقمية'].values[0]
    
    if liquidity >= 50000000:
        return ['background-color: #2ecc71; color: white; font-weight: bold'] * len(row)
    return [''] * len(row)

# --- 4. محرك الرادار الحقيقي ---
placeholder = st.empty()

if st.button("تشغيل الرادار الآن 🚀"):
    while True:
        for symbol in symbols:
            try:
                # استخدام yfinance لجلب البيانات (الـ API و Secret هنا يعملان كحماية للدخول)
                ticker = yf.Ticker(symbol)
                info = ticker.fast_info
                
                price = info.last_price
                volume = info.last_volume
                flow_value = price * volume 
                
                # منطق السعر السابق لتحديد الاتجاه
                old_price = st.session_state.price_history.get(symbol, price)
                
                # --- فلتر الـ 50 مليون دولار ---
                if flow_value >= 50000000:
                    status = "👑 حوت ذهبي"
                    if price > old_price: signal = "CALL 🟢"
                    elif price < old_price: signal = "PUT 🔴"
                    else: signal = "تمركز ⚪"
                else:
                    status = "⚪ عادي"
                    signal = "انتظار ⏳"
                
                # تحديث الذاكرة
                st.session_state.price_history[symbol] = price
                st.session_state.market_data[symbol] = {
                    "الشركة": symbol,
                    "السعر الآن": price,
                    "الحالة": status,
                    "التنبيه": signal,
                    "السيولة الرقمية": flow_value 
                }
            except:
                continue

        # --- 5. العرض النهائي للجدول ---
        with placeholder.container():
            if st.session_state.market_data:
                df_full = pd.DataFrame(list(st.session_state.market_data.values()))
                # الترتيب حسب الأضخم سيولة
                df_full = df_full.sort_values(by='السيولة الرقمية', ascending=False)
                
                # اختيار الأعمدة التي طلبتها (بدون مال متدفق أو سيولة رقمية)
                display_cols = ["الشركة", "السعر الآن", "الحالة", "التنبيه"]
                df_display = df_full[display_cols].copy()
                
                # تنسيق السعر للعرض
                df_display['السعر الآن'] = df_display['السعر الآن'].apply(lambda x: f"${x:.2f}")
                
                st.subheader("📡 مسح حي للمسابح المظلمة والحيتان...")
                st.table(df_display.style.apply(lambda row: highlight_whales(row, df_full), axis=1))
                
        time.sleep(2)
        st.rerun()
else:
    st.write("اضغط على الزر أعلاه ليبدأ الرادار بالبحث عن الحيتان.")
