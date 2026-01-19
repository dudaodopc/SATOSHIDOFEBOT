import telebot
import os
import requests

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise Exception("BOT_TOKEN não encontrado nas variáveis de ambiente")

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(
        msg,
        "🤖 SATOSHIDOFEBOT está online!\n\n"
        "Comandos disponíveis:\n"
        "/btc - Preço do Bitcoin"
    )


@bot.message_handler(commands=['btc'])
def btc(msg):
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

        response = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        response.raise_for_status()

        data = response.json()
        price = float(data["price"])

        bot.send_message(
            msg.chat.id,
            f"🟠 BITCOIN (BTC)\n\n"
            f"Preço atual: ${price:.2f}\n"
            f"Fonte: Binance"
        )

except Exception as e:
    bot.send_message(
        msg.chat.id,
        f"⚠️ Erro ao buscar dados do BTC\n\n"
        f"Erro real:\n{repr(e)}"
    )

print("Bot iniciado...")
bot.infinity_polling(skip_pending=True)
