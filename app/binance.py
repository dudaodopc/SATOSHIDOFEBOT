import requests

BASE_URL = "https://api.binance.com/api/v3"

def get_ticker(symbol: str):
    symbol = symbol.upper() + "USDT"

    price_url = f"{BASE_URL}/ticker/24hr?symbol={symbol}"
    price_resp = requests.get(price_url).json()

    if "code" in price_resp:
        return None

    return {
        "symbol": symbol,
        "price": float(price_resp["lastPrice"]),
        "change": float(price_resp["priceChangePercent"]),
        "volume": float(price_resp["quoteVolume"])
    }
