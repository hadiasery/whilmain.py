import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
import time

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="رادار هادي اللحظي ⚡", layout="wide")

# تثبيت العنوان في الأعلى
st.title("🎯 رادار هادي (تحديث مباشر ومستقر)")
st.write("✅ الجدول الآن ثابت والتحديث يتم داخلياً بالثانية.")

# قائمة الأسهم 
symbols = ["PLTR", "SOFI", "NIO", "MARA", "TSLA", "AAPL", "NVDA", "RIVN"]

# استخدام session_state لتخزين البيانات لضمان عدم اختفائها عند التحديث
if 'whale_history' not in st.session_state:
    st.session_state.whale_history = []

# --- 2. تجهيز حاوية الجدول الثابتة ---
# هذه الحاوية ستبقى ثابتة في الصفحة ويتم تحديث ما بداخلها فقط
table_placeholder = st.empty()

# --- 3. حلقة التحديث المستمر ---
while True:
    for symbol in symbols:
        try:
            # جلب البيانات اللحظية
            ticker = yf.Ticker(symbol)
            info = ticker.fast_info
            current_price = info.last_price
            
            # فلتر السعر (تحت 500$ لمراقبة السوق بشكل عام)
            if 0 < current_price <= 500:
                new_entry = {
                    "الوقت": datetime.datetime.now().strftime("%H:%M:%S"),
                    "السهم": symbol,
                    "السعر الآن": f"${current_price:.2f}",
                    "الحالة": "مباشر ✅"
                }
                
                # إضافة البيانات الجديدة في أعلى القائمة
                st.session_state.whale_history.insert(0, new_entry)
                
                # الاحتفاظ بآخر 15 حركة فقط لمنع ثقل الصفحة
                st.session_state.whale_history = st.session_state.whale_history[:15]
            
            # تحديث الجدول داخل الحاوية الثابتة فوراً بعد كل سهم
            with table_placeholder.container():
                if st.session_state.whale_history:
                    df = pd.DataFrame(st.session_state.whale_history)
                    # عرض الجدول بدون الفهرس الجانبي (Index) ليكون أجمل
                    st.table(df)
                    
            # وقت انتظار قصير جداً بين فحص الأسهم ليكون التحديث سريعاً
            time.sleep(0.1) 
            
        except:
            continue

    # انتظار بسيط قبل بدء دورة الفحص التالية لضمان عدم تعليق المتصفح
    time.sleep(1)
