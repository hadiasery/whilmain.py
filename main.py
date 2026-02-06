import streamlit as st
import pandas as pd
import yfinance as yf
import time

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="رادار هادي - قناص المليون 🐳", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stTable { background-color: white; border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 رادار هادي (قناص صفقات المليون)")
st.write("📊 التنبيه: +1,000,000$ | الترتيب: حسب قوة السيولة | الحالة: مباشر")

# قائمة الشركات
symbols = ["PLTR", "SOFI", "NIO", "MARA", "TSLA", "AAPL", "NVDA", "RIVN", "AMD", "AMC"]

if 'market_data' not in st.session_state:
    st.session_state.market_data = {}
if 'price_history' not in st.session_state:
    st.session_state.price_history = {}

table_placeholder = st.empty()

# --- 2. دالة التلوين (تعديل القيمة إلى 1,000,000) ---
def highlight_whales(row):
    # استخدام القيمة الرقمية من البيانات الأصلية لتحديد التلوين
    liquidity = row.get('السيولة الرقمية', 0)
    if isinstance(liquidity, (int, float)) and liquidity >= 1000000:
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
            
            # تحديد الاتجاه بناءً على السعر اللحظي
            old_price = st.session_state.price_history.get(symbol, price)
            if flow_value >= 1000000:
                if price > old_price: signal = "🐳 CALL 🟢"
                elif price < old_price: signal = "🐳 PUT 🔴"
                else: signal = "🐳 WHALE ⚪"
            else:
                signal = "⏳ WAIT"
            
            st.session_state.price_history[symbol] = price
            
            # تخزين البيانات
            st.session_state.market_data[symbol] = {
                "الشركة": symbol,
                "السعر الآن": price,
                "المال المتدفق": f"${flow_value:,.0f}",
                "التنبيه": signal,
                "السيولة الرقمية": flow_value # للحساب والترتيب فقط
            }
        except:
            continue

    # --- 4. العرض النهائي (بدون عمود السيولة الرقمية) ---
    with table_placeholder.container():
        if st.session_state.market_data:
            df = pd.DataFrame(list(st.session_state.market_data.values()))
            
            if 'السيولة الرقمية' in df.columns:
                # ترتيب الجدول حسب السيولة (الأعلى أولاً)
                df = df.sort_values(by='السيولة الرقمية', ascending=False)
                
                # تجهيز نسخة العرض وتنسيق الأسعار
                df_display = df.copy()
                df_display['السعر الآن'] = df_display['السعر الآن'].apply(lambda x: f"${x:.2f}")
                
                # اختيار الأعمدة المراد إظهارها فقط (حذف السيولة الرقمية من العرض)
                final_columns = ["الشركة", "السعر الآن", "المال المتدفق", "التنبيه"]
                
                # عرض الجدول المنسق
                st.table(
                    df_display[final_columns + ["السيولة الرقمية"]]
                    .style.apply(highlight_whales, axis=1)
                    .hide(axis="columns", subset=["السيولة الرقمية"])
                )

    time.sleep(2)
