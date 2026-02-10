import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

from zerodha import get_kite
from indicators import add_indicators

# -------------------------------
# Streamlit Page Config
# -------------------------------
st.set_page_config(
    page_title="Bank Nifty Analyzer",
    layout="wide"
)

st.title("📊 Bank Nifty Advanced Analyzer")

# -------------------------------
# Zerodha Connection
# -------------------------------
kite = get_kite()

# -------------------------------
# Bank Nifty LTP
# -------------------------------
try:
    ltp = kite.ltp("NSE:NIFTY BANK")["NSE:NIFTY BANK"]["last_price"]
    st.metric("Bank Nifty LTP", ltp)
except Exception as e:
    st.error("Unable to fetch Bank Nifty LTP")
    st.stop()

# -------------------------------
# Bank Nifty Index Token (Fixed)
# -------------------------------
BN_TOKEN = 260105   # Zerodha official Bank Nifty index token

# -------------------------------
# Historical Data (Last 5 Days)
# -------------------------------
to_date = datetime.now()
from_date = to_date - timedelta(days=5)

try:
    data = kite.historical_data(
        instrument_token=BN_TOKEN,
        from_date=from_date,
        to_date=to_date,
        interval="5minute"
    )
except Exception as e:
    st.error("Error fetching historical data from Zerodha")
    st.stop()

df = pd.DataFrame(data)

if df.empty:
    st.error("No historical data received")
    st.stop()

# -------------------------------
# Add Indicators
# -------------------------------
df = add_indicators(df)

# -------------------------------
# Charts
# -------------------------------
st.subheader("📈 Price & Moving Averages")

st.line_chart(
    df[["close", "ma20", "ma50", "ma200"]],
    height=400
)

# -------------------------------
# Momentum Indicators
# -------------------------------
st.subheader("⚡ Momentum Indicators")

rsi_val = round(df["rsi"].iloc[-1], 2)
willr_val = round(df["willr"].iloc[-1], 2)

col1, col2 = st.columns(2)
col1.metric("RSI", rsi_val)
col2.metric("Williams %R", willr_val)

# -------------------------------
# Market Bias
# -------------------------------
st.subheader("🧠 Market Bias")

if rsi_val > 70:
    st.error("Overbought – Pullback Possible")
elif rsi_val < 30:
    st.success("Oversold – Bounce Possible")
else:
    st.info("Neutral / Range-Bound Market")
