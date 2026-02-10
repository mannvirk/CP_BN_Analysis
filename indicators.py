
import ta

def add_indicators(df):
    df["rsi"] = ta.momentum.RSIIndicator(df["close"]).rsi()
    df["willr"] = ta.momentum.WilliamsRIndicator(
        df["high"], df["low"], df["close"]
    ).williams_r()

    df["ma20"] = df["close"].rolling(20).mean()
    df["ma50"] = df["close"].rolling(50).mean()
    df["ma200"] = df["close"].rolling(200).mean()
    return df
