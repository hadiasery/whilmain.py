import yfinance as yf
import pandas as pd

def find_silent_accumulation(ticker_list):
    print("🔎 جاري مسح السوق بحثاً عن تراكم صامت...")
    for ticker in ticker_list:
        stock = yf.Ticker(ticker)
        
        # 1. فحص حركة السعر (نبحث عن استقرار/ضيق)
        hist = stock.history(period="5d")
        price_range = (hist['High'].max() - hist['Low'].min()) / hist['Close'].iloc[-1]
        
        # 2. فحص الأوبشن (نبحث عن عقود تزيد فيها OI بهدوء)
        try:
            opt_dates = stock.options[0:3] # فحص أقرب 3 تواريخ انتهاء
            for date in opt_dates:
                chain = stock.option_chain(date)
                # الثغرة: عقود OI فيها عالي جداً مقارنة بحجم التداول والسعر ثابت
                hot_calls = chain.calls[(chain.calls['openInterest'] > 5000) & 
                                       (chain.calls['volume'] < chain.calls['openInterest'] * 0.1)]
                
                if not hot_calls.empty and price_range < 0.03: # إذا كان تذبذب السعر أقل من 3%
                    print(f"⚠️ تنبيه: سهم {ticker} يظهر علامات تراكم صامت عند سترايك {hot_calls['strike'].values}")
        except:
            continue

# قائمة بأسهم للمراقبة (يمكنك إضافة أي سهم هنا)
watch_list = ["AAPL", "TSLA", "AMD", "MSFT", "NVDA", "GOOGL"]
find_silent_accumulation(watch_list)
