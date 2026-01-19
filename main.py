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
        "📊 Monitoramento cripto em tempo real\n\n"
        "⚔️ <b>Comandos:</b>\n"
        "/btc – Bitcoin\n"
        "/eth – Ethereum\n"
        "/top – Top moedas do dia\n"
        "/rompimentos – Moedas em forte movimento\n"
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
        "/top – Top moedas 24h\n"
        "/rompimentos – Possíveis rompimentos"
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
            f"💰 Preço: <b>${price:,.2f}</b>\n"
            "📡 Fonte: CoinGecko"
        )
    except:
        bot.send_message(msg.chat.id, "⚠️ Erro ao buscar BTC")

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
            f"💰 Preço: <b>${price:,.2f}</b>\n"
            "📡 Fonte: CoinGecko"
        )
    except:
        bot.send_message(msg.chat.id, "⚠️ Erro ao buscar ETH")

# ================= TOP MOEDAS =================
@bot.message_handler(commands=['top'])
def top(msg):
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/coins/markets",
            params={
                "vs_currency": "usd",
                "order": "price_change_percentage_24h_desc",
                "per_page": 5,
                "page": 1
            },
            timeout=10
        )
        r.raise_for_status()

        coins = r.json()

        text = "🚀 <b>TOP MOEDAS DO DIA (24h)</b>\n\n"

        for c in coins:
            name = c["name"]
            symbol = c["symbol"].upper()
            change = c["price_change_percentage_24h"]
            price = c["current_price"]

            text += (
                f"🔥 <b>{name} ({symbol})</b>\n"
                f"💰 ${price:,.4f}\n"
                f"📈 {change:.2f}%\n\n"
            )

        bot.send_message(msg.chat.id, text)

    except Exception as e:
        bot.send_message(msg.chat.id, "⚠️ Erro ao buscar top moedas")
        print("ERRO TOP:", e)

# ================= ROMPIMENTOS =================
@bot.message_handler(commands=['rompimentos'])
def rompimentos(msg):
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/coins/markets",
            params={
                "vs_currency": "usd",
                "order": "volume_desc",
                "per_page": 10,
                "page": 1
            },
            timeout=10
        )
        r.raise_for_status()

        coins = r.json()

        text = "💥 <b>POSSÍVEIS ROMPIMENTOS</b>\n"
        text += "<i>Baseado em volume + variação</i>\n\n"

        for c in coins:
            change = c["price_change_percentage_24h"]
            if change and change > 8:
                text += (
                    f"⚡ <b>{c['name']} ({c['symbol'].upper()})</b>\n"f"📈 {change:.2f}%\n"
                    f"💰 ${c['current_price']:,.4f}\n\n"
                )

        if text.strip().endswith(":\n\n"):
            text += "Nenhum rompimento forte detectado agora."

        bot.send_message(msg.chat.id, text)

    except Exception as e:
        bot.send_message(msg.chat.id, "⚠️ Erro ao buscar rompimentos")
        print("ERRO ROMPIMENTOS:", e)

# ================= RUN =================
print("🤖 Bot iniciado com sucesso")
bot.infinity_polling(skip_pending=True)
