from binance.client import Client

client = Client()

def get_price(symbol: str):
    data = client.get_symbol_ticker(symbol=symbol)
    return data["price"]
