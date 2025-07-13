import requests, datetime as dt

class CryptoPriceTool:
    name = "get_crypto_price"
    description = "Retorna preço, variação 24h e market-cap de um token."

    def __call__(self, symbol: str) -> dict:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": symbol.lower(),
            "vs_currencies": "usd",
            "include_24hr_change": "true",
            "include_market_cap": "true",
        }
        data = requests.get(url, params=params, timeout=10).json().get(symbol.lower(), {})
        return {
            "symbol": symbol.upper(),
            "price": data.get("usd"),
            "change_24h": data.get("usd_24hr_change"),
            "market_cap": data.get("usd_market_cap"),
            "ts": dt.datetime.utcnow().isoformat(),
        }
