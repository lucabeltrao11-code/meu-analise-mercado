import requests
import pandas as pd
import time

def get_crypto_price_history(coin, days, retries=5, delay=10):
    """
    Busca histórico de preços no CoinGecko com retry automático em caso de 429.
    """
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
    params = {"vs_currency": "usd", "days": days}

    for attempt in range(retries):
        r = requests.get(url, params=params)
        if r.status_code == 429:
            print(f"Limite de requisições atingido. Tentando novamente em {delay}s...")
            time.sleep(delay)
            continue
        r.raise_for_status()
        prices = r.json()["prices"]
        return pd.DataFrame(prices, columns=["timestamp", "price"])
    
    # Se falhar após todas as tentativas
    raise Exception("Não foi possível obter dados da CoinGecko após várias tentativas.")
