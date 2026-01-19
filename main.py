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
        "/btc — Preço do Bitcoin"
    )

@bot.message_handler(commands=['btc', 'BTC'])
def btc(msg):
    try:
        url = "https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            bot.reply_to(msg, "⚠️ Binance indisponível no momento")
            return

        r = response.json()

        price = float(r["lastPrice"])
        change = float(r["priceChangePercent"])
        volume = float(r["volume"])

        text = (
            "🟠 *BITCOIN (BTC)*\n\n"
            f"💰 Preço: ${price:,.2f}\n"
            f"📊 Variação 24h: {change:.2f}%\n"
            f"🔄 Volume 24h: {volume:,.0f} BTC\n\n"
            "_Dados via Binance_"
        )

        bot.send_message(msg.chat.id, text, parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(msg, "⚠️ Erro ao buscar dados do BTC")
        print("ERRO BTC:", e)

print("Bot iniciado...")
bot.infinity_polling()
