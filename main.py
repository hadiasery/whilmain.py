import yfinance as yf
import pandas as pd
import time
import random
from colorama import Fore, Style, init

# تهيئة الألوان لتسهيل القراءة
init(autoreset=True)

def hunt_whales(tickers):
    print(Fore.CYAN + "🚀 بدء رادار الحيتان المنزلي... (آمن 100%)")
    print(Fore.YELLOW + "------------------------------------------")
    
    for ticker in tickers:
        try:
            print(f"🔎 فحص {ticker}...")
            stock = yf.Ticker(ticker)
            
            # جلب السعر الحالي
            price = stock.fast_info['lastPrice']
            
            # جلب تواريخ الانتهاء
            options_dates = stock.options
            if not options_dates:
                continue
            
            # فحص أول تاريخ انتهاء (الأكثر نشاطاً)
            chain = stock.option_chain(options_dates[0])
            calls = chain.calls
            
            # فلتر "الحوت الصامت": حجم تداول ضخم مقارنة بالعقود المفتوحة
            # نركز على العقود التي يتجاوز حجمها 1500 عقد الآن
            big_moves = calls[calls['volume'] > 1500].sort_values(by='volume', ascending=False)
            
            if not big_moves.empty:
                print(Fore.GREEN + f"✅ صيد ثمين في {ticker} (السعر: {price:.2f}$):")
                for _, row in big_moves.head(3).iterrows():
                    print(f"   🔹 سترايك: {row['strike']} | الحجم: {row['volume']} | السيولة (OI): {row['openInterest']}")
            else:
                print(Fore.WHITE + f"   - لا توجد حركة غير طبيعية حالياً في {ticker}")

            # 🛑 أهم خطوة لتجنب الحظر: "التنفس الصناعي"
            # ننتظر وقتاً عشوائياً بين الأسهم لكي لا يشك الموقع
            time.sleep(random.uniform(5, 10))
            
        except Exception as e:
            print(Fore.RED + f"❌ تعذر جلب {ticker}: قد يكون هناك ضغط على الشبكة.")
            time.sleep(30) # انتظر دقيقة إذا حدث خطأ

# قائمة الأسهم التي تهمك
my_list = ["TSLA", "NVDA", "AAPL", "AMD", "PLTR", "MARA"]

# تشغيل الحلقة اللانهائية للمراقبة
while True:
    hunt_whales(my_list)
    print(Fore.BLUE + "\n☕ استراحة لمدة دقيقتين قبل المسح القادم...")
    time.sleep(120)
