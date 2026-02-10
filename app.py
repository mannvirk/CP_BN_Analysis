
import streamlit as st
import pandas as pd
from zerodha import get_kite
from indicators import add_indicators

st.set_page_config(page_title="Bank Nifty Analyzer", layout="wide")
st.title("📊 Bank Nifty Advanced Analyzer")

kite = get_kite()

ltp = kite.ltp("NSE:NIFTY BANK")["NSE:NIFTY BANK"]["last_price"]
st.metric("Bank Nifty LTP", ltp)

inst = kite.instruments("NSE")
token = [i for i in inst if i["tradingsymbol"] == "BANKNIFTY"][0]["instrument_token"]

data = kite.historical_data(token, interval="5minute", days=5)
df = pd.DataFrame(data)
df = add_indicators(df)

st.subheader("📈 Price & Moving Averages")
st.line_chart(df[["close", "ma20", "ma50", "ma200"]])

st.subheader("⚡ Momentum")
st.write("RSI:", round(df["rsi"].iloc[-1], 2))
st.write("Williams %R:", round(df["willr"].iloc[-1], 2))

if df["rsi"].iloc[-1] > 70:
    st.error("Overbought – Pullback Possible")
elif df["rsi"].iloc[-1] < 30:
    st.success("Oversold – Bounce Possible")
else:
    st.info("Neutral Zone")
