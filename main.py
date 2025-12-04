from fastapi import FastAPI
from price_fetcher import get_crypto_price_history
from indicators import analyze_asset

app = FastAPI(title="Sistema de Análise de Mercado")

@app.get("/")
def home():
    return {"status": "online", "message": "API de Análise de Mercado funcionando!"}


@app.get("/analisar/{cripto}")
def analisar_cripto(cripto: str, dias: int = 30):
    """
    Ex.: /analisar/bitcoin?dias=90
    """
   # Opcionalmente, pode usar cache automático
    data = get_crypto_price_history(cripto, dias)
    analise = analyze_asset(data)
    return analise
