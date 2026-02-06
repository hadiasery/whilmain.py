import streamlit as st
import pandas as pd
import yfinance as yf
import time

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="رادار هادي - صيد الحيتان 🐳", layout="wide")

# تصحيح الخطأ هنا: تم تغيير الكلمة إلى unsafe_allow_html
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stTable { background-color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 رادار هادي المطوّر (تنبيه الحيتان بالألوان)")
st.write("✅ الجدول مرتب حسب السعر، واللون الأخضر يظهر عند دخول سيولة كبيرة.")

# قائمة الشركات
symbols = ["PLTR", "SOFI", "NIO", "MARA", "TSLA", "AAPL", "NVDA", "RIVN", "AMD"]

if 'market_data' not in st.session_state:
    st.session_state.market_data = {}

table_placeholder = st.empty()

# --- 2. دالة تلوين الصفوف ---
def highlight_whales(row):
    # إذا كانت السيولة أكبر من 50,000$ يتلون الصف بالأخضر
    if row['السيولة الرقمية'] >= 50000:
        return ['background-color: #d4edda; color: #155724; font-weight: bold'] * len(row)
    return [''] * len(row)

# --- 3. حلقة الرصد والتحديث ---
while True:
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.fast_info
            
            price = info.last_price
            volume = info.last_volume
            # حساب السيولة المتدفقة (القيمة الإجمالية لآخر تداول)
            flow_value = price * volume 
            
            # تحديث البيانات في الذاكرة
            st.session_state.market_data[symbol] = {
                "الشركة": symbol,
                "السعر الآن": price,
                "السيولة المتدفقة": f"${flow_value:,.0f}",
                "السيولة الرقمية": flow_value, # عمود مخفي للفرز والتلوين
                "الحالة": "🐳 حوت مكتشف!" if flow_value >= 50000 else "مراقبة.."
            }
            
            # عرض الجدول الملون والثابت
            with table_placeholder.container():
                if st.session_state.market_data:
                    df = pd.DataFrame(st.session_state.market_data.values())
                    
                    # ترتيب: الأعلى سعراً أولاً
                    df = df.sort_values(by='السعر الآن', ascending=False)
                    
                    # تنسيق العرض
                    df_display = df.copy()
                    df_display['السعر الآن'] = df_display['السعر الآن'].apply(lambda x: f"${x:.2f}")
                    
                    # استبعاد العمود الرقمي من العرض النهائي ليكون الجدول مرتباً
                    display_cols = ["الشركة", "السعر الآن", "السيولة المتدفقة", "الحالة", "السيولة الرقمية"]
                    styled_df = df_display[display_cols].style.apply(highlight_whales, axis=1)
                    
                    st.table(styled_df)
            
            time.sleep(0.1)
        except:
            continue
