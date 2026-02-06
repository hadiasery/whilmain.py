import streamlit as st
import pandas as pd
import requests
import datetime
import time

# --- 1. إعدادات الواجهة ---
st.set_page_config(page_title="رادار هادي - القناص الذكي", layout="wide")
st.title("🎯 رادار هادي: صيد الحيتان (أسهم تحت 50$)")
st.write(f"🔍 الرادار يراقب الآن الأسهم التي يمكنك شراؤها بميزانية 50 دولار.")

# --- 2. إعدادات البيانات والمفتاح الخاص بك ---
API_KEY = "A8nb_XrU0KTykEls_e6tgpg9D6iZZVQt"

# قائمة الأسهم النشطة والرخيصة (اقتصادية)
symbols = ["PLTR", "SOFI", "NIO", "F", "LCID", "CCL", "T", "PFE", "AAL"]

if 'whale_history' not in st.session_state:
    st.session_state.whale_history = []

# --- 3. وظيفة الرصد المستمر ---
def scan_market():
    for symbol in symbols:
        # جلب بيانات آخر صفقة للسهم
        url = f"https://api.polygon.io/v2/last/trade/{symbol}?apiKey={API_KEY}"
        try:
            r = requests.get(url)
            if r.status_code == 200:
                data = r.json().get('results', {})
                price = data.get('p', 0)  # السعر الحالي
                size = data.get('s', 0)   # كمية الأسهم في الصفقة
                value = price * size      # القيمة الإجمالية للصفقة
                
                # الفلتر: السعر تحت 50$ والقيمة الإجمالية للصفقة فوق 20,000$ (دخول حوت)
                if 0 < price <= 50 and value >= 20000:
                    trade = {
                        "الوقت": datetime.datetime.now().strftime("%H:%M:%S"),
                        "السهم": symbol,
                        "سعر السهم": f"${price:.2f}",
                        "قيمة صفقة الحوت": f"${value:,.0f} 🐳",
                        "الحالة": "متاح للشراء ✅"
                    }
                    
                    # إضافة الصيد الجديد ومنع التكرار اللحظي
                    if not st.session_state.whale_history or st.session_state.whale_history[0]['قيمة صفقة الحوت'] != trade['قيمة صفقة الحوت']:
                        st.session_state.whale_history.insert(0, trade)
                        # الاحتفاظ بآخر 15 صيداً فقط لتنظيم الشاشة
                        st.session_state.whale_history = st.session_state.whale_history[:15]
            
            # تأخير لمدة 12 ثانية لتجنب تجاوز حد الـ 5 طلبات في الدقيقة (للنسخة المجانية)
            time.sleep(12) 
        except:
            continue

# --- 4. عرض النتائج على الصفحة ---
placeholder = st.empty()

# بدء الحلقة اللانهائية للرصد المستمر
while True:
    scan_market()
    with placeholder.container():
        if st.session_state.whale_history:
            # تحويل البيانات لجدول أنيق
            df = pd.DataFrame(st.session_state.whale_history)
            st.table(df)
        else:
            st.info("الرادار يمسح الأسهم الاقتصادية الآن... يرجى الانتظار لصيد أول حوت 🌊")
    
    # تحديث واجهة Streamlit تلقائياً
    st.rerun()
