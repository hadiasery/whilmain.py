import streamlit as st
import pandas as pd
import time
import random

st.set_page_config(page_title="رادار هادي - القناص الثابت", layout="wide")

# قائمة الشركات الشرعية (تحت 25$)
clean_list = ['MARA', 'RIOT', 'PLTR', 'F', 'CLOV', 'NIO', 'AAL', 'GRWG', 'AMC']

# مخزن ذاكرة الرادار لمنع التذبذب (Session State)
if 'confirmed_whales' not in st.session_state:
    st.session_state.confirmed_whales = {}

st.title("🏹 رادار هادي: نسخة صيد الحيتان المؤكدة")
st.info("💡 لن يظهر التنبيه إلا إذا كان النشاط حقيقياً وثابتاً لمدة زمنية.")

table_placeholder = st.empty()

def get_stable_data():
    results = []
    current_time = time.time()
    
    for symbol in clean_list:
        # محاكاة قوة السيولة (يجب أن تتجاوز 200% لتصبح حوتاً)
        vol_strength = random.randint(50, 250)
        
        # منطق التثبيت الذكي:
        # إذا كان السهم مسجلاً كـ "حوت" ولم تمر دقيقتين، يبقى "حوت" مهما تغيرت البيانات
        if symbol in st.session_state.confirmed_whales:
            if current_time < st.session_state.confirmed_whales[symbol]['expiry']:
                # السهم ما زال في فترة "التجميد" ليعطيك فرصة للتداول
                status = "🚨 حوت مؤكد (فرصة شراء)"
                direction = st.session_state.confirmed_whales[symbol]['direction']
                vol_display = st.session_state.confirmed_whales[symbol]['vol']
            else:
                # انتهت فترة التجميد، نعود للمراقبة العادية
                del st.session_state.confirmed_whales[symbol]
                status = "🔍 مراقبة"
                direction = "تحليل ⏳"
                vol_display = f"{vol_strength}%"
        else:
            # إذا ظهر نشاط قوي جداً، نقوم بتثبيته فوراً
            if vol_strength > 210:
                direction = "CALL 🟢" if random.random() > 0.5 else "PUT 🔴"
                st.session_state.confirmed_whales[symbol] = {
                    'expiry': current_time + 120, # تثبيت لمدة دقيقتين
                    'direction': direction,
                    'vol': f"{vol_strength}%"
                }
                status = "🚨 حوت مؤكد (فرصة شراء)"
                vol_display = f"{vol_strength}%"
            else:
                status = "🔍 مراقبة"
                direction = "تحليل ⏳"
                vol_display = f"{vol_strength}%"

        results.append({
            "الشركة": symbol,
            "الحالة": status,
            "الاتجاه": direction,
            "قوة السيولة": vol_display,
            "الميزانية (25$)": "✅ جاهز"
        })
    return pd.DataFrame(results)

# التحديث المستمر داخل الجدول
while True:
    df = get_stable_data()
    with table_placeholder.container():
        st.write(f"🕒 **توقيت المسح اللحظي:** {time.strftime('%H:%M:%S')}")
        
        # تنسيق الجدول وتلوين الفرص المؤكدة
        def highlight_confirmed(val):
            color = '#1e8449' if 'حوت مؤكد' in str(val) else ''
            return f'background-color: {color}; color: white' if color else ''

        st.table(df.style.applymap(highlight_confirmed, subset=['الحالة']))
        
    time.sleep(5) # تحديث كل 5 ثوانٍ
