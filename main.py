import telebot
import os
import requests

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(
        msg,
        "🤖 SATOSHIDOFEBOT está online!\n\n"
        "Comandos disponíveis:\n"
        "/btc - Preço do Bitcoin"
    )

@bot.message_handler(commands=['btc', 'BTC'])
def btc(msg):
    try:
        # Binance
        url = "https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            r = response.json()
            price = float(r["lastPrice"])
            change = float(r["priceChangePercent"])
            volume = float(r["volume"])
            source = "Binance"
        else:
            raise Exception("Binance falhou")

    except Exception:
        try:
            # CoinGecko
            url = "https://api.coingecko.com/api/v3/coins/markets"
            params = {"vs_currency": "usd", "ids": "bitcoin"}
            response = requests.get(url, params=params, timeout=10)

            r = response.json()[0]
            price = r["current_price"]
            change = r["price_change_percentage_24h"]
            volume = r["total_volume"]
            source = "CoinGecko"

        except Exception as e:
            bot.reply_to(msg, "⚠️ Erro ao buscar dados do BTC")
            print("ERRO REAL:", e)
            return

    text = (
        "🟠 BITCOIN (BTC)\n\n"
        f"Preço: ${price:.2f}\n"
        f"Variação 24h: {change:.2f}%\n"
        f"Volume 24h: ${int(volume)}\n\n"
        f"Fonte: {source}"
    )

    bot.send_message(msg.chat.id, text)

print("Bot iniciado...")
bot.infinity_polling(skip_pending=True)
