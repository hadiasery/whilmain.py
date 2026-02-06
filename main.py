import streamlit as st
from ib_insync import *
import pandas as pd
import datetime

# --- إعدادات الواجهة ---
st.set_page_config(page_title="رادار الحيتان - القناص", layout="wide")
st.title("🐳 رادار صيد ونسخ صفقات الحيتان")

# --- إدارة الحالة (Session State) ---
if 'whale_trades' not in st.session_state:
    st.session_state.whale_trades = []

# --- دالة تنفيذ الصفقة ---
def place_whale_order(symbol, quantity):
    try:
        contract = Stock(symbol, 'SMART', 'USD')
        ib.qualifyContracts(contract)
        # أمر شراء بسعر السوق (Market Order) للحاق بالحوت سريعاً
        order = MarketOrder('BUY', quantity)
        trade = ib.placeOrder(contract, order)
        st.success(f"🚀 تم إرسال أمر شراء {quantity} سهم في {symbol} بنجاح!")
    except Exception as e:
        st.error(f"❌ فشل التنفيذ: {e}")

# --- الاتصال بـ IBKR ---
@st.cache_resource
def get_ib_connection():
    ib_instance = IB()
    try:
        ib_instance.connect('127.0.0.1', 7497, clientId=15)
        return ib_instance
    except:
        return None

ib = get_ib_connection()

if not ib:
    st.warning("⚠️ يرجى التأكد من تشغيل TWS أو IB Gateway وتفعيل الـ API")
else:
    # --- القائمة الجانبية ---
    st.sidebar.header("إعدادات الرادار")
    whale_limit = st.sidebar.number_input("حد الصفقة (دولار)", value=100000, step=10000)
    copy_size = st.sidebar.number_input("كمية النسخ (عدد الأسهم)", value=10, step=1)
    
    # --- رصد البيانات ---
    symbols = ['TSLA', 'NVDA', 'AAPL', 'AMD', 'MSFT', 'SPY']
    contracts = [Stock(s, 'SMART', 'USD') for s in symbols]
    ib.qualifyContracts(*contracts)

    def onTick(tickers):
        for ticker in tickers:
            if ticker.lastSize and ticker.last:
                val = ticker.last * ticker.lastSize
                if val >= whale_limit:
                    trade_data = {
                        "الوقت": datetime.datetime.now().strftime("%H:%M:%S"),
                        "السهم": ticker.contract.symbol,
                        "السعر": ticker.last,
                        "القيمة": val
                    }
                    if trade_data not in st.session_state.whale_trades:
                        st.session_state.whale_trades.insert(0, trade_data)
                        st.session_state.whale_trades = st.session_state.whale_trades[:10]

    for c in contracts:
        ib.reqMktData(c, '', False, False)
    
    ib.pendingTickersEvent += onTick

    # --- عرض الجدول مع أزرار التنفيذ ---
    st.subheader("📊 الصفقات المرصودة حالياً")
    
    if st.session_state.whale_trades:
        for i, trade in enumerate(st.session_state.whale_trades):
            cols = st.columns([1, 1, 1, 1, 2])
            cols[0].write(trade['الوقت'])
            cols[1].write(f"**{trade['السهم']}**")
            cols[2].write(f"${trade['السعر']}")
            cols[3].write(f"${trade['القيمة']:,.0f}")
            
            # زر النسخ لكل صفقة
            if cols[4].button(f"نسخ صفقة {trade['السهم']} 🎯", key=f"btn_{i}"):
                place_whale_order(trade['السهم'], copy_size)
    else:
        st.info("الرادار يعمل في الخفاء.. بانتظار الحيتان 🌊")

    # تحديث تلقائي للواجهة
    ib.sleep(0.5)
    st.rerun()
