import streamlit as st
from yahooquery import Ticker
import pandas as pd

st.title("🕵️ رادار الحيتان - النسخة المصفحة")

symbol = st.text_input("أدخل السهم:", "NVDA")

if st.button('بدء المسح الآن 🚀'):
    try:
        # استخدام التيكر عبر مكتبة yahooquery (أصعب في الكشف)
        t = Ticker(symbol)
        
        # جلب بيانات الأوبشن
        df = t.option_chain
        
        if df is not None and not df.empty:
            st.success(f"✅ تم سحب البيانات بنجاح من IP المنصة الجديد!")
            
            # ترتيب حسب أعلى حجم تداول لرؤية الحيتان
            # لاحظ أن الفهرس هنا مختلف قليلاً في هذه المكتبة
            df_sorted = df.sort_values(by='volume', ascending=False).head(10)
            st.dataframe(df_sorted[['strike', 'lastPrice', 'volume', 'openInterest']])
        else:
            st.warning("لم تظهر بيانات، قد يكون السهم لا يملك عقوداً نشطة حالياً.")
            
    except Exception as e:
        st.error(f"⚠️ حدثت مشكلة: {e}")
