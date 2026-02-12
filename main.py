import pandas as pd
import requests

def barchart_whale_scanner():
    # هذا الرابط يذهب مباشرة لجدول الخيارات غير الطبيعية
    url = "https://www.barchart.com/options/unusual-daily-volume"
    
    # هوية متصفح كاملة لتجنب الحظر
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }

    try:
        # ملاحظة: برشارط يحتاج أحياناً لزيارة الصفحة الرئيسية أولاً لأخذ "كوكي"
        session = requests.Session()
        session.get("https://www.barchart.com", headers=headers)
        
        # الآن نطلب البيانات
        response = session.get(url, headers=headers)
        
        # قراءة الجداول من الصفحة
        tables = pd.read_html(response.text)
        df = tables[0] # الجدول الأول عادة هو جدول الصفقات
        
        print("🎯 تم صيد الصفقات غير الطبيعية من Barchart:")
        print(df[['Symbol', 'Price', 'Strike', 'Volume', 'Open Int']].head(10))
        
    except Exception as e:
        print(f"⚠️ الموقع اكتشفنا أو الجدول تغير هيلكله.. نحتاج لتكتيك أعمق.")

barchart_whale_scanner()
