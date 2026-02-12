import yfinance as yf
import time
import random
import requests_cache

# إعداد "ذاكرة مؤقتة" لتقليل عدد الطلبات
session = requests_cache.CachedSession('yfinance.cache')
session.headers['User-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

def find_silent_accumulation_pro(ticker_list):
    print("🕵️ جاري التسلل بهدوء لسحب البيانات...")
    for ticker in ticker_list:
        try:
            # استخدام الجلسة المموّهة
            stock = yf.Ticker(ticker, session=session)
            
            # فحص السعر
            hist = stock.history(period="5d")
            if hist.empty: continue
            
            price_range = (hist['High'].max() - hist['Low'].min()) / hist['Close'].iloc[-1]
            
            # فحص الأوبشن
            opt_dates = stock.options[0:2] # تقليل عدد الطلبات لفحص أول تاريخين فقط
            for date in opt_dates:
                chain = stock.option_chain(date)
                
                # معيار التراكم: OI عالي جداً مع تداول منخفض
                hot_calls = chain.calls[(chain.calls['openInterest'] > 2000) & 
                                       (chain.calls['volume'] < chain.calls['openInterest'] * 0.05)]
                
                if not hot_calls.empty and price_range < 0.04:
                    print(f"💰 صيد ثمين: {ticker} | سترايك: {hot_calls['strike'].values[0]} | السعر ثابت.")
            
            # 🛑 "النفس المجنون": الانتظار لفترة عشوائية بين 3 إلى 7 ثواني لتجنب الحظر
            wait_time = random.uniform(3, 7)
            time.sleep(wait_time)
            
        except Exception as e:
            print(f"❌ تعذر فحص {ticker} حالياً.. سننتقل للتالي.")
            time.sleep(10) # انتظار أطول عند حدوث خطأ
            continue

# جرب القائمة ببطء الآن
watch_list = ["AAPL", "TSLA", "NVDA", "AMD"]
find_silent_accumulation_pro(watch_list)
