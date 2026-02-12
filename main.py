import pandas as pd
import requests
import time

def stealth_whale_hunt(ticker):
    # محاكاة متصفح حقيقي 100%
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,ir/apng,*/*;q=0.8',
    }
    
    # رابط البيانات الخام (نطلب بيانات الأوبشن مباشرة)
    url = f"https://query1.finance.yahoo.com/v7/finance/options/{ticker}"
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()
        
        # استخراج عقود الـ Calls
        calls = data['optionChain']['result'][0]['options'][0]['calls']
        df = pd.DataFrame(calls)
        
        # ترتيب حسب الحجم (Volume) لرؤية أين يضع الحيتان أموالهم الآن
        top_moves = df[['strike', 'lastPrice', 'volume', 'openInterest']].sort_values(by='volume', ascending=False)
        
        print(f"\n🎯 تم اختراق البيانات لسهم: {ticker}")
        print(top_moves.head(5)) # إظهار أعلى 5 عقود نشاطاً
        
    except Exception as e:
        print(f"❌ فشل التسلل لسهم {ticker}: المصدر يرفض الاستجابة.")

# جرب سهمين فقط للتأكد من نجاح "الاختراق"
for t in ["TSLA", "NVDA"]:
    stealth_whale_hunt(t)
    time.sleep(2) # انتظار بسيط
