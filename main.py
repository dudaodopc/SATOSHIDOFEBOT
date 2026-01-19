import telebot
import os
import requests

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise Exception("BOT_TOKEN não encontrado")

bot = telebot.TeleBot(TOKEN)

# ================= START =================
@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(
        msg,
        "🤖 *SATOSHIDOFEBOT está online!*\n\n"
        "📊 Comandos disponíveis:\n"
        "/btc — Preço do Bitcoin",
        parse_mode="Markdown"
    )

# ================= BTC =================
@bot.message_handler(commands=['btc', 'BTC'])
def btc(msg):
    try:
        # ===== BINANCE =====
        url = "https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            r = response.json()

            price = float(r["lastPrice"])
            change = float(r["priceChangePercent"])
            volume = float(r["volume"])
            source = "Binance"

        else:
            raise Exception("Binance bloqueou")

    except Exception:
        # ===== COINGECKO (endpoint correto) =====
        try:
            url = "https://api.coingecko.com/api/v3/coins/markets"
            params = {
                "vs_currency": "usd",
                "ids": "bitcoin"
            }

            response = requests.get(url, params=params, timeout=10)

            if response.status_code != 200:
                raise Exception("CoinGecko indisponível")

            r = response.json()[0]

            price = r["current_price"]
            change = r["price_change_percentage_24h"]
            volume = r["total_volume"]
            source = "CoinGecko"

        except Exception as e:
            bot.reply_to(msg, "⚠️ Erro ao buscar dados do BTC")
            print("ERRO FINAL BTC:", e)
            return

    text = (
        "🟠 *BITCOIN (BTC)*\n\n"
        f"💰 *Preço:* ${price:,.2f}\n"
        f"📊 *Variação 24h:* {change:.2f}%\n"
        f"📦 *Volume 24h:* ${volume:,.0f}\n\n"
        f"_Fonte: {source}_"
    )

    bot.send_message(msg.chat.id, text, parse_mode="Markdown")

# ================= RUN =================
print("🤖 Bot iniciado...")
bot.infinity_polling(skip_pending=True)
