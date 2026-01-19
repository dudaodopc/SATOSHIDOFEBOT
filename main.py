import telebot
import os
import requests

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise Exception("BOT_TOKEN não encontrado")

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(
        msg,
        "🤖 SATOSHIDOFEBOT está online!\n\n"
        "Comandos disponíveis:\n"
        "/btc — Preço do Bitcoin"
    )


@bot.message_handler(commands=['btc'])
def btc(msg):
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "bitcoin",
            "vs_currencies": "usd"
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        price = data["bitcoin"]["usd"]

        bot.send_message(
            msg.chat.id,
            f"🟠 *BITCOIN (BTC)*\n\n"
            f"💰 Preço atual: *${price:,.2f}*\n"
            f"_Fonte: CoinGecko_",
            parse_mode="Markdown"
        )

    except Exception as e:
        bot.send_message(
            msg.chat.id,
            f"⚠️ Erro ao buscar dados do BTC\n{repr(e)}"
        )
        print("ERRO REAL:", repr(e))


print("Bot iniciado...")
bot.infinity_polling(skip_pending=True)
