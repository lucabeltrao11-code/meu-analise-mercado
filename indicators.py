import pandas as pd
import numpy as np

def rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def macd(series):
    ema12 = series.ewm(span=12, adjust=False).mean()
    ema26 = series.ewm(span=26, adjust=False).mean()
    macd_line = ema12 - ema26
    signal = macd_line.ewm(span=9, adjust=False).mean()
    hist = macd_line - signal
    return macd_line, signal, hist

def analyze_asset(df):
    df["SMA20"] = df["price"].rolling(20).mean()
    df["RSI"] = rsi(df["price"])
    df["MACD"], df["Signal"], df["Hist"] = macd(df["price"])

    current_price = float(df["price"].iloc[-1])
    current_rsi = float(df["RSI"].iloc[-1])
    current_macd = float(df["MACD"].iloc[-1])
    current_signal = float(df["Signal"].iloc[-1])

    # Recomendação simples
    if current_rsi < 30 and current_macd > current_signal:
        recomendacao = "Possível oportunidade de COMPRA"
    elif current_rsi > 70 and current_macd < current_signal:
        recomendacao = "Possível sinal de VENDA"
    else:
        recomendacao = "Mercado neutro / aguardando melhor momento"

    return {
        "preco_atual": current_price,
        "RSI": f"{current_rsi:.2f}",
        "MACD": f"{current_macd:.4f}",
        "Signal": f"{current_signal:.4f}",
        "Recomendação": recomendacao
    }
