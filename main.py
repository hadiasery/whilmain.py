import yfinance as yf
import time
import random

def find_silent_accumulation_stealth(ticker_list):
    print("🕵️ جاري التسلل باستخدام تقنية 'المراوغة'...")
    
    for ticker in ticker_list:
        try:
            # تمويه الطلب ليبدو كأنه من متصفح مختلف في كل مرة
            stock = yf.Ticker(ticker)
            
            # جلب البيانات
            hist = stock.history(period="5d")
            if hist.empty:
                continue
            
            # حساب التذبذب (نبحث عن ضيق السعر)
            volatility = (hist['High'].max() - hist['Low'].min()) / hist['Close'].iloc[-1]
            
            # فحص عقود الأوبشن
            dates = stock.options
            if not dates: continue
            
            chain = stock.option_chain(dates[0])
            
            # فلتر الحيتان: OI عالي جداً وحجم تداول منخفض (تراكم صامت)
            # ركزنا هنا على العقود التي يفوق فيها OI الحجم بـ 10 أضعاف
            stealth_moves = chain.calls[(chain.calls['openInterest'] > 1000) & 
                                        (chain.calls['volume'] < chain.calls['openInterest'] * 0.1)]
            
            if not stealth_moves.empty and volatility < 0.05:
                print(f"✅ كشفنا حركة صامتة في {ticker}!")
                print(f"   السترايك: {stealth_moves.iloc[0]['strike']} | السيولة المفتوحة: {stealth_moves.iloc[0]['openInterest']}")

            # "نفس عميق" لتضليل خوارزميات الحظر
            time.sleep(random.randint(5, 10))
            
        except Exception as e:
            print(f"⚠️ ياهو تحاول الحظر عند {ticker}.. سآخذ استراحة.")
            time.sleep(20)

# قائمة صغيرة للبدء بها
watch_list = ["PLTR", "TSLA", "NVDA", "BABA"]
find_silent_accumulation_stealth(watch_list)
