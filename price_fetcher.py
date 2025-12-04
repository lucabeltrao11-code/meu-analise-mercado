import requests
import pandas as pd

def get_crypto_price_history(coin: str, days: int):
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
    params = {"vs_currency": "usd", "days": days}

    r = requests.get(url, params=params)
    r.raise_for_status()
    prices = r.json()["prices"]

    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df
