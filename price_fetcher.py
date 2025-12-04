# price_fetcher.py

import requests
import pandas as pd
import time
from functools import lru_cache

@lru_cache(maxsize=32)
def get_crypto_price_history(coin, days, retries=5, delay=10):
    """
    Busca histórico de preços no CoinGecko com retry automático em caso de 429 (Too Many Requests).
    O resultado é cacheado em memória para reduzir chamadas repetidas.
    
    Parâmetros:
    - coin: string, nome da cripto (ex: "bitcoin")
    - days: int, quantidade de dias de histórico
    - retries: int, número de tentativas em caso de erro 429
    - delay: int, segundos de espera entre tentativas
    """

    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
    params = {"vs_currency": "usd", "days": days}

    for attempt in range(retries):
        try:
            r = requests.get(url, params=params)
            if r.status_code == 429:
                print(f"[Aviso] Limite de requisições atingido. Tentativa {attempt+1}/{retries}. Aguardando {delay}s...")
                time.sleep(delay)
                continue
            r.raise_for_status()
            prices = r.json()["prices"]
            # Retorna dataframe com timestamp e preço
            return pd.DataFrame(prices, columns=["timestamp", "price"])
        except requests.RequestException as e:
            print(f"[Erro] Falha na requisição: {e}")
            time.sleep(delay)
    
    # Se falhar após todas as tentativas
    raise Exception(f"Não foi possível obter dados da CoinGecko para {coin} após {retries} tentativas.")
