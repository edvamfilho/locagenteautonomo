import os
import sys
import requests
from openai import OpenAI
from dotenv import load_dotenv

# Carregar chave da OpenAI
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Função que consulta preço no CoinGecko


def get_crypto_price(symbol):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": symbol.lower(),
        "vs_currencies": "usd",
        "include_24hr_change": "true",
        "include_market_cap": "true",
    }
    r = requests.get(url, params=params, timeout=10).json().get(
        symbol.lower(), {})
    return {
        "symbol": symbol.upper(),
        "price": r.get("usd"),
        "change_24h": r.get("usd_24hr_change"),
        "market_cap": r.get("usd_market_cap"),
    }

# Função principal do agente


def chat(pergunta):
    SYSTEM = """
    Você é o Lab Onchain, agente educador em Web3, cripto, NFTs e DeFi. Responda sempre em português do Brasil.
    Se te perguntarem o preço de alguma cripto, diga o preço em dólares, market cap e variação 24h.
    """
    client = OpenAI(api_key=OPENAI_API_KEY)

    # Gatilho manual: se detectar palavra "preço" e nome de moeda
    if "preço" in pergunta.lower() or "cotação" in pergunta.lower():
        for moeda in ["bitcoin", "btc", "ethereum", "eth", "solana", "sol"]:
            if moeda in pergunta.lower():
                result = get_crypto_price(moeda)
                return f"Preço do {result['symbol']}: ${result['price']} | Variação 24h: {result['change_24h']}% | Market Cap: ${result['market_cap']}"
    # Senão, usa o GPT-4o-mini para responder
    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": pergunta}
        ]
    )
    return resposta.choices[0].message.content


# CLI simples
if __name__ == "__main__":
    pergunta = " ".join(sys.argv[1:]) or input("Pergunte: ")
    print(chat(pergunta))
