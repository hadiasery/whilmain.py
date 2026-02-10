import streamlit as st
import yfinance as yf
import pandas as pd
import time

# 1. إعداد الصفحة (بدون أي أزرار بدء)
st.set_page_config(page_title="رادار هادي اللحظي", layout="wide")

# 2. القائمة الشرعية فقط + الميزانية تحت 25$ (تم حذف NVDA, TSLA, AAPL, SOFI, LCID)
final_watch_list = ['MARA', 'RIOT', 'PLTR', 'F', 'CLOV', 'NIO', 'AAL', 'GRWG', 'AMC']

st.title("🏹 رادار هادي - نظام القنص الذاتي")
st.write("---")
st.success("✅ الرادار يعمل الآن بشكل آلي تماماً (بدون أزرار) ويراقب الشركات الشرعية فقط.")

# حاوية الجدول
placeholder = st.empty()

def start_scanning():
    results = []
    for symbol in final_watch_list:
        try:
            ticker = yf.Ticker(symbol)
            # جلب البيانات اللحظية
            data = ticker.history(period='1d', interval='1m').tail(5)
            if data.empty: continue

            last_price = data.iloc[-1]['Close']
            prev_price = data.iloc[-2]['Close']
            current_vol = data.iloc[-1]['Volume']
            avg_vol = data['Volume'].mean()
            
            vol_strength = (current_vol / avg_vol) * 100
            
            # تحديد الاتجاه واللون
            direction = "CALL 🟢" if last_price > prev_price else "PUT 🔴"
            status = "👑 حوت ذهبي" if vol_strength > 150 else "⚪ عادي"
            
            results.append({
                "الشركة": symbol,
                "السعر الآن": f"${round(last_price, 2)}",
                "الحالة": status,
                "التنبيه": direction,
                "قوة السيولة": f"{round(vol_strength)}%",
                "الميزانية": "✅ متاح بـ 25$"
            })
        except:
            continue
    return pd.DataFrame(results)

# --- محرك التشغيل الأوتوماتيكي المباشر ---
while True:
    df_results = start_scanning()
    with placeholder.container():
        st.write(f"⏱️ **تحديث مباشر:** {time.strftime('%H:%M:%S')}")
        if not df_results.empty:
            # تلوين الجدول بالكامل بالأخضر عند رصد حوت كما في صورتك
            def highlight_whale(row):
                if "حوت" in row['الحالة']:
                    return ['background-color: #2ecc71; color: white'] * len(row)
                return [''] * len(row)
            
            st.table(df_results.style.apply(highlight_whale, axis=1))
        else:
            st.warning("🔎 جاري جلب البيانات من السوق...")
            
    # تحديث كل 5 ثوانٍ تلقائياً
    time.sleep(5)
    st.rerun()
