import yfinance as yf
import pandas as pd
import streamlit as st

def crazy_scanner():
    st.write("🔎 جاري فحص الرادار... إذا لم تظهر نتائج، فالموقع يحجبنا.")
    
    # قائمة أسهم قوية للبدء
    tickers = ["TSLA", "NVDA", "AAPL", "AMD", "PLTR", "MARA"]
    found_something = False

    for ticker in tickers:
        try:
            # محاولة جلب البيانات بأكثر من طريقة
            tk = yf.Ticker(ticker)
            opts = tk.options
            
            if not opts:
                st.warning(f"⚠️ {ticker}: لم نجد عقود أوبشن حالياً.")
                continue
                
            # جلب أول تاريخ انتهاء
            chain = tk.option_chain(opts[0])
            calls = chain.calls
            
            # فلتر الحيتان: حجم التداول > 1000 عقد (حركة نشطة جداً)
            whales = calls[calls['volume'] > 1000].sort_values(by='volume', ascending=False)
            
            if not whales.empty:
                found_something = True
                st.success(f"✅ تم رصد حيتان في {ticker}")
                st.table(whales[['strike', 'lastPrice', 'volume', 'openInterest']].head(5))
                
        except Exception as e:
            st.error(f"❌ خطأ في {ticker}: {str(e)}")

    if not found_something:
        st.info("ℹ️ الرادار يعمل ولكن لا توجد صفقات ضخمة (Volume > 1000) في هذه اللحظة.")

# تشغيل الرادار
if st.button('ابدأ استراق السمع الآن'):
    crazy_scanner()
