import yfinance as yf
import pandas as pd

def fast_scan_no_limits(ticker_list):
    print("🚀 جاري المسح السريع.. سنمسح القيود لنرى الحيتان الآن:")
    results = []
    
    for ticker in ticker_list:
        try:
            stock = yf.Ticker(ticker)
            # جلب أقرب تاريخ انتهاء (أكثر سيولة)
            options = stock.options
            if not options:
                continue
            
            chain = stock.option_chain(options[0])
            calls = chain.calls
            
            # فلتر "أقل قسوة" لإظهار النتائج: 
            # نبحث عن أي عقد فيه حجم التداول (Volume) أكبر من 500 عقد 
            # وهو ما يمثل حركة "غير طبيعية" للساعة الحالية
            unusual = calls[calls['volume'] > 500].sort_values(by='volume', ascending=False)
            
            if not unusual.empty:
                for index, row in unusual.head(3).iterrows():
                    results.append({
                        'Ticker': ticker,
                        'Strike': row['strike'],
                        'Volume': row['volume'],
                        'OI': row['openInterest'],
                        'Last Price': row['lastPrice']
                    })
                    print(f"✅ وجدنا حركة في {ticker} - سترايك {row['strike']} - حجم: {row['volume']}")
        except Exception as e:
            print(f"❌ {ticker}: لا توجد استجابة من المصدر.")
            
    return pd.DataFrame(results)

# لنضع قائمة أكبر لضمان صيد شيء ما
test_list = ["TSLA", "NVDA", "AMD", "AAPL", "MSFT", "META", "AMZN", "PLTR", "BABA", "MARA"]
df = fast_scan_no_limits(test_list)

if df.empty:
    print("\n⚠️ لا تزال البيانات محجوبة.. ياهو ترفض إعطاء معلومات الأوبشن حالياً.")
else:
    print("\n🎯 تقرير الحيتان المبدئي:")
    print(df)
