import streamlit as st
import yfinance as yf
import pandas as pd

st.title("🛡️ رادار الأوبشن - نسخة الإنقاذ")

ticker = st.text_input("أدخل رمز السهم (مثلاً AAPL):", "TSLA")

if st.button('بدء الفحص الآمن'):
    try:
        # 1. طلب البيانات بهدوء
        stock = yf.Ticker(ticker)
        
        # 2. جلب أقرب تاريخ انتهاء (السيولة الأعلى)
        dates = stock.options
        if dates:
            chain = stock.option_chain(dates[0])
            calls = chain.calls
            
            # 3. فلتر الحيتان: حجم التداول (Volume) أكبر من 1000
            whales = calls[calls['volume'] > 1000].sort_values(by='volume', ascending=False)
            
            if not whales.empty:
                st.success(f"✅ تم العثور على تحركات ضخمة في {ticker}")
                st.dataframe(whales[['strike', 'lastPrice', 'volume', 'openInterest']])
            else:
                st.info("لا توجد عقود بحجم تداول ضخم حالياً لهذا السهم.")
        else:
            st.warning("لم يتم العثور على بيانات أوبشن حالياً.")
            
    except Exception as e:
        if "Rate limited" in str(e):
            st.error("🛑 تم حظر الـ IP الخاص بالمنصة. يرجى الانتظار 10 دقائق أو التشغيل محلياً.")
        else:
            st.error(f"حدث خطأ غير متوقع: {e}")
