import streamlit as st
import pandas as pd
import yfinance as yf
import time

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="رادار هادي - قناص الحيتان 🐳", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stTable { background-color: white; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 رادار هادي (قناص الصفقات الكبرى)")
st.write("📊 التنبيه: +5,000,000$ | الترتيب: حسب المال المتدفق | الحالة: مباشر")

# الشركات المختارة
symbols = ["PLTR", "SOFI", "NIO", "MARA", "TSLA", "AAPL", "NVDA", "RIVN", "AMD", "AMC"]

if 'market_data' not in st.session_state:
    st.session_state.market_data = {}
if 'price_history' not in st.session_state:
    st.session_state.price_history = {}

table_placeholder = st.empty()

# --- 2. دالة التلوين (تم رفع القيمة إلى 5 مليون لتقليل اللون الأخضر الزائد) ---
def highlight_whales(row, df_original):
    symbol = row['الشركة']
    # جلب القيمة الحقيقية للتحقق من الشرط
    liquidity = df_original.loc[df_original['الشركة'] == symbol, 'السيولة الرقمية'].values[0]
    
    if liquidity >= 5000000:
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
            
            # منطق التنبيه (CALL/PUT/WAIT)
            old_price = st.session_state.price_history.get(symbol, price)
            if flow_value >= 5000000:
                if price > old_price: signal = "🐳 CALL 🟢"
                elif price < old_price: signal = "🐳 PUT 🔴"
                else: signal = "🐳 WHALE ⚪"
            else:
                signal = "⏳ WAIT"
            
            st.session_state.price_history[symbol] = price
            st.session_state.market_data[symbol] = {
                "الشركة": symbol,
                "السعر الآن": price,
                "المال المتدفق": f"${flow_value:,.0f}",
                "التنبيه": signal,
                "السيولة الرقمية": flow_value 
            }
        except:
            continue

    # --- 4. العرض النهائي (أعمدة محددة فقط) ---
    with table_placeholder.container():
        if st.session_state.market_data:
            df_full = pd.DataFrame(list(st.session_state.market_data.values()))
            df_full = df_full.sort_values(by='السيولة الرقمية', ascending=False)
            
            # إنشاء نسخة للعرض تحتوي فقط على الأعمدة الـ 4 المطلوبة
            # تم حذف "السيولة الرقمية" تماماً من هنا
            df_display = df_full[["الشركة", "السعر الآن", "المال المتدفق", "التنبيه"]].copy()
            df_display['السعر الآن'] = df_display['السعر الآن'].apply(lambda x: f"${x:.2f}")
            
            # تطبيق التلوين باستخدام المرجع الأصلي (df_full) ثم العرض
            st.table(df_display.style.apply(lambda row: highlight_whales(row, df_full), axis=1))

    time.sleep(2)
