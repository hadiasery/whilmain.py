import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
import time

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="رادار هادي - ترتيب الأسعار ⚡", layout="wide")

st.title("🎯 رادار هادي (مرتب حسب الأعلى سعراً)")
st.write("✅ يتم الآن ترتيب الجدول تلقائياً ليظهر السهم الأغلى في الأعلى.")

# قائمة الأسهم 
symbols = ["PLTR", "SOFI", "NIO", "MARA", "TSLA", "AAPL", "NVDA", "RIVN", "AMD"]

if 'whale_history' not in st.session_state:
    st.session_state.whale_history = []

# حاوية الجدول الثابتة
table_placeholder = st.empty()

# --- 2. حلقة التحديث المستمر ---
while True:
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.fast_info
            current_price = info.last_price
            
            if 0 < current_price <= 500:
                # أضفنا السعر كقيمة رقمية (Float) للفرز وقيمة نصية للعرض
                new_entry = {
                    "الوقت": datetime.datetime.now().strftime("%H:%M:%S"),
                    "السهم": symbol,
                    "السعر": current_price, # قيمة رقمية للترتيب
                    "الحالة": "مباشر ✅"
                }
                
                # إضافة السهم وتحديث القائمة
                # ملاحظة: نحدث سعر السهم إذا كان موجوداً بالفعل أو نضيفه كجديد
                found = False
                for i, entry in enumerate(st.session_state.whale_history):
                    if entry['السهم'] == symbol:
                        st.session_state.whale_history[i] = new_entry
                        found = True
                        break
                if not found:
                    st.session_state.whale_history.append(new_entry)
            
            # --- 3. عملية الترتيب والعرض ---
            with table_placeholder.container():
                if st.session_state.whale_history:
                    # تحويل القائمة إلى DataFrame
                    df = pd.DataFrame(st.session_state.whale_history)
                    
                    # ترتيب الجدول حسب عمود 'السعر' تنازلياً (الأعلى أولاً)
                    df = df.sort_values(by='السعر', ascending=False)
                    
                    # تحسين شكل السعر للعرض بإضافة علامة $
                    df_display = df.copy()
                    df_display['السعر'] = df_display['السعر'].apply(lambda x: f"${x:.2f}")
                    
                    st.table(df_display)
                    
            time.sleep(0.1) 
            
        except:
            continue

    time.sleep(1)
