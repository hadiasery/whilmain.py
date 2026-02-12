import yfinance as yf
import time
import random

def safe_radar(tickers):
    print("🛡️ تشغيل الرادار بنمط 'التخفي الآمن'...")
    for ticker in tickers:
        try:
            # استخدام مكتبة yfinance مع وقت انتظار عشوائي
            stock = yf.Ticker(ticker)
            
            # جلب البيانات التاريخية (أقل ضغطاً من بيانات الأوبشن)
            data = stock.history(period="1d", interval="1m")
            
            if not data.empty:
                current_price = data['Close'].iloc[-1]
                print(f"✅ {ticker}: السعر الحالي {current_price}")
            
            # 🛑 "قانون الصبر": انتظر بين 10 إلى 20 ثانية بين كل سهم
            wait = random.uniform(10, 20)
            time.sleep(wait)
            
        except Exception as e:
            print(f"⚠️ تنبيه: ياهو تطلب منا الهدوء. سننتظر دقيقة.")
            time.sleep(60)

# ابدأ بأسهم قليلة جداً لتأمين الـ IP الخاص بك
safe_radar(["TSLA", "NVDA", "AAPL"])
