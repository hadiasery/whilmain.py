import streamlit as st
import pandas as pd
import yfinance as yf
import time

# --- 1. إعدادات الصفحة والجمالية ---
st.set_page_config(page_title="رادار هادي - صيد الحيتان 🐳", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stTable { background-color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_status_code=True)

st.title("🎯 رادار هادي المطوّر (تنبيه الحيتان بالألوان)")
st.write("✅ الأخضر يعني: دخول سيولة كبيرة (حوت) الآن!")

# قائمة الشركات
symbols = ["PLTR", "SOFI", "NIO", "MARA", "TSLA", "AAPL", "NVDA", "RIVN", "AMD"]

if 'market_data' not in st.session_state:
    st.session_state.market_data = {}

table_placeholder = st.empty()

# --- 2. دالة تلوين الصفوف ---
def highlight_whales(row):
    # إذا كانت السيولة المتدفقة (القيمة) أكبر من 50,000 دولار نعتبره حوت ونلون الصف
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
            # حساب السيولة المتدفقة التقديرية (السعر * حجم آخر صفقة)
            flow_value = price * volume 
            
            # تحديث بيانات الشركة في الـ Session
            st.session_state.market_data[symbol] = {
                "الشركة": symbol,
                "السعر الآن": price,
                "السيولة المتدفقة": f"${flow_value:,.0f}",
                "السيولة الرقمية": flow_value, # مخفي للفرز والتلوين
                "الحالة": "🐳 حوت مكتشف!" if flow_value >= 50000 else "مراقبة.."
            }
            
            # عرض وتحديث الجدول
            with table_placeholder.container():
                if st.session_state.market_data:
                    # تحويل البيانات لجدول
                    df = pd.DataFrame(st.session_state.market_data.values())
                    
                    # الترتيب: الأعلى سعراً أولاً كما طلبت
                    df = df.sort_values(by='السعر الآن', ascending=False)
                    
                    # تحسين شكل السعر للعرض
                    df_display = df.copy()
                    df_display['السعر الآن'] = df_display['السعر الآن'].apply(lambda x: f"${x:.2f}")
                    
                    # تطبيق التلوين الأخضر عند اكتشاف حوت
                    styled_df = df_display.style.apply(highlight_whales, axis=1)
                    
                    # إخفاء العمود الرقمي المستخدم للحسابات فقط
                    st.table(styled_df)
            
            time.sleep(0.1) # سرعة المسح
            
        except:
            continue
