import telebot
import os
import requests
import time

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN não configurado")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# ================= START =================
@bot.message_handler(commands=["start"])
def start(msg):
    bot.send_message(
        msg.chat.id,
        "🤖 <b>SATOSHIDOFEBOT ONLINE</b>\n\n"
        "📊 Monitoramento do mercado cripto\n\n"
        "⚔️ <b>Comandos:</b>\n"
        "/btc – Preço do Bitcoin\n"
        "/eth – Preço do Ethereum\n"
        "/dominance – Dominância do BTC\n"
        "/fear – Fear & Greed Index\n"
        "/top – Top moedas do dia\n"
        "/rompimentos – Possíveis rompimentos\n"
        "/ajuda – Lista completa"
    )

# ================= AJUDA =================
@bot.message_handler(commands=["ajuda"])
def ajuda(msg):
    start(msg)

# ================= BTC =================
@bot.message_handler(commands=["btc"])
def btc(msg):
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd",
            timeout=10
        )
        price = r.json()["bitcoin"]["usd"]
        bot.send_message(msg.chat.id, f"🟠 <b>BITCOIN</b>\n💰 ${price:,.2f}")
    except:
        bot.send_message(msg.chat.id, "⚠️ Erro ao buscar BTC")

# ================= ETH =================
@bot.message_handler(commands=["eth"])
def eth(msg):
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd",
            timeout=10
        )
        price = r.json()["ethereum"]["usd"]
        bot.send_message(msg.chat.id, f"🔵 <b>ETHEREUM</b>\n💰 ${price:,.2f}")
    except:
        bot.send_message(msg.chat.id, "⚠️ Erro ao buscar ETH")

# ================= TOP MOEDAS =================
@bot.message_handler(commands=["top"])
def top(msg):
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/coins/markets",
            params={
                "vs_currency": "usd",
                "order": "market_cap_desc",
                "per_page": 5,
                "page": 1
            },
            headers=HEADERS,
            timeout=10
        )

        data = r.json()
        if not isinstance(data, list):
            raise ValueError("Resposta inválida")

        text = "🏆 <b>TOP MOEDAS</b>\n\n"
        for c in data:
            text += f"• <b>{c['name']}</b> ({c['symbol'].upper()})\n💰 ${c['current_price']:,.2f}\n\n"

        bot.send_message(msg.chat.id, text)

    except Exception as e:
        bot.send_message(msg.chat.id, "⚠️ Erro ao buscar TOP moedas")
        print("ERRO TOP:", repr(e))

# ================= ROMPIMENTOS (BLINDADO) =================
@bot.message_handler(commands=["rompimentos"])
def rompimentos(msg):
    bot.send_message(msg.chat.id, "🔍 Analisando possíveis rompimentos...")

    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/coins/markets",
            params={
                "vs_currency": "usd",
                "order": "volume_desc",
                "per_page": 20,
                "page": 1
            },
            headers=HEADERS,
            timeout=10
        )

        coins = r.json()

        if not isinstance(coins, list):
            bot.send_message(msg.chat.id, "⚠️ CoinGecko indisponível no momento")
            return

        encontrados = 0
        text = "🚀 <b>POSSÍVEIS ROMPIMENTOS</b>\n<i>Volume + variação 24h</i>\n\n"

        for c in coins:
            change = c.get("price_change_percentage_24h")
            if isinstance(change, (int, float)) and change >= 8:
                encontrados += 1
                text += (
                    f"🔥 <b>{c['name']}</b> ({c['symbol'].upper()})\n"
                    f"📈 {change:.2f}% | 💰 ${c['current_price']:,.4f}\n\n"
                )

        if encontrados == 0:
            text += "😴 Nenhum rompimento forte no momento."

        bot.send_message(msg.chat.id, text)

    except Exception as e:
        bot.
