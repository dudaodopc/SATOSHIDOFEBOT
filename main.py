import telebot
import os
import requests

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise Exception("BOT_TOKEN não encontrado")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# ================= START =================
@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(
        msg.chat.id,
        "🤖 <b>SATOSHIDOFEBOT ONLINE</b>\n\n"
        "📊 Monitoramento do mercado cripto em tempo real\n\n"
        "⚔️ <b>Comandos iniciais:</b>\n"
        "/btc – Preço do Bitcoin\n"
        "/eth – Preço do Ethereum\n"
        "/dominance – Dominância do BTC\n"
        "/fear – Fear & Greed Index\n"
        "/ajuda – Lista completa"
    )

# ================= AJUDA =================
@bot.message_handler(commands=['ajuda'])
def ajuda(msg):
    bot.send_message(
        msg.chat.id,
        "🧭 <b>AJUDA</b>\n\n"
        "/btc – Preço do Bitcoin\n"
        "/eth – Preço do Ethereum\n"
        "/dominance – Dominância do BTC\n"
        "/fear – Sentimento do mercado"
    )

# ================= BTC =================
@bot.message_handler(commands=['btc'])
def btc(msg):
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={"ids": "bitcoin", "vs_currencies": "usd"},
            timeout=10
        )
        r.raise_for_status()
        price = r.json()["bitcoin"]["usd"]

        bot.send_message(
            msg.chat.id,
            f"🟠 <b>BITCOIN (BTC)</b>\n\n"
            f"💰 Preço atual: <b>${price:,.2f}</b>\n"
            "📡 Fonte: CoinGecko"
        )
    except Exception as e:
        bot.send_message(msg.chat.id, "⚠️ Erro ao buscar dados do BTC")
        print("ERRO BTC:", e)

# ================= ETH =================
@bot.message_handler(commands=['eth'])
def eth(msg):
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={"ids": "ethereum", "vs_currencies": "usd"},
            timeout=10
        )
        r.raise_for_status()
        price = r.json()["ethereum"]["usd"]

        bot.send_message(
            msg.chat.id,
            f"🔵 <b>ETHEREUM (ETH)</b>\n\n"
            f"💰 Preço atual: <b>${price:,.2f}</b>\n"
            "📡 Fonte: CoinGecko"
        )
    except Exception as e:
        bot.send_message(msg.chat.id, "⚠️ Erro ao buscar dados do ETH")
        print("ERRO ETH:", e)

# ================= DOMINANCE =================
@bot.message_handler(commands=['dominance'])
def dominance(msg):
    try:
        r = requests.get("https://api.coingecko.com/api/v3/global", timeout=10)
        r.raise_for_status()
        btc_dom = r.json()["data"]["market_cap_percentage"]["btc"]

        bot.send_message(
            msg.chat.id,
            f"📊 <b>DOMINÂNCIA DO BITCOIN</b>\n\n"
            f"🟠 BTC: <b>{btc_dom:.2f}%</b>"
        )
    except Exception as e:
        bot.send_message(msg.chat.id, "⚠️ Erro ao buscar dominância")
        print("ERRO DOMINANCE:", e)

# ================= FEAR & GREED =================
@bot.message_handler(commands=['fear'])
def fear(msg):
    try:
        r = requests.get("https://api.alternative.me/fng/", timeout=10)
        r.raise_for_status()

        data = r.json()["data"][0]
        value = data["value"]
        status = data["value_classification"]

        bot.send_message(
            msg.chat.id,
            f"😱 <b>FEAR & GREED INDEX</b>\n\n"
            f"📈 Índice: <b>{value}</b>\n"
            f"🧠 Sentimento: <b>{status}</b>"
        )
    except Exception as e:
        bot.send_message(msg.chat.id, "⚠️ Erro ao buscar Fear & Greed")
        print("ERRO FEAR:", e)

# ================= RUN =================
print("🤖 Bot iniciado com sucesso")
bot.infinity_polling(skip_pending=True)
