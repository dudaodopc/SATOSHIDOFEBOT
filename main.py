import telebot
import requests
import os

# ================= CONFIG =================

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise Exception("BOT_TOKEN não encontrado")

bot = telebot.TeleBot(TOKEN)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (SatoshidofeBot)"
}

# ================= START =================

@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(
        msg.chat.id,
        "🤖 <b>SATOSHIDOFEBOT ONLINE</b>\n\n"
        "📊 Monitoramento do mercado cripto\n\n"
        "⚔️ <b>Comandos:</b>\n"
        "/btc - Preço do Bitcoin\n"
        "/eth - Preço do Ethereum\n"
        "/dominance - Dominância do BTC\n"
        "/fear - Fear & Greed Index\n"
        "/top - Top moedas do dia\n"
        "/rompimentos - Possíveis rompimentos\n"
        "/ajuda - Lista completa",
        parse_mode="HTML"
    )

# ================= AJUDA =================

@bot.message_handler(commands=['ajuda'])
def ajuda(msg):
    bot.send_message(
        msg.chat.id,
        "🧭 <b>AJUDA</b>\n\n"
        "/btc\n/eth\n/dominance\n/fear\n/top\n/rompimentos",
        parse_mode="HTML"
    )

# ================= BTC =================

@bot.message_handler(commands=['btc'])
def btc(msg):
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd",
            headers=HEADERS,
            timeout=10
        )
        price = r.json()["bitcoin"]["usd"]
        bot.send_message(msg.chat.id, f"🟠 <b>BTC</b>\n💰 ${price:,.2f}", parse_mode="HTML")
    except Exception as e:
        bot.send_message(msg.chat.id, "⚠️ Erro ao buscar BTC")
        print("ERRO BTC:", repr(e))

# ================= ETH =================

@bot.message_handler(commands=['eth'])
def eth(msg):
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd",
            headers=HEADERS,
            timeout=10
        )
        price = r.json()["ethereum"]["usd"]
        bot.send_message(msg.chat.id, f"🔵 <b>ETH</b>\n💰 ${price:,.2f}", parse_mode="HTML")
    except Exception as e:
        bot.send_message(msg.chat.id, "⚠️ Erro ao buscar ETH")
        print("ERRO ETH:", repr(e))

# ================= DOMINANCE =================

@bot.message_handler(commands=['dominance'])
def dominance(msg):
    try:
        r = requests.get("https://api.coingecko.com/api/v3/global", headers=HEADERS, timeout=10)
        btc_dom = r.json()["data"]["market_cap_percentage"]["btc"]
        bot.send_message(msg.chat.id, f"📊 <b>Dominância BTC</b>\n🟠 {btc_dom:.2f}%", parse_mode="HTML")
    except Exception as e:
        bot.send_message(msg.chat.id, "⚠️ Erro ao buscar dominância")
        print("ERRO DOM:", repr(e))

# ================= FEAR =================

@bot.message_handler(commands=['fear'])
def fear(msg):
    try:
        r = requests.get("https://api.alternative.me/fng/", timeout=10)
        data = r.json()["data"][0]
        bot.send_message(
            msg.chat.id,
            f"😱 <b>Fear & Greed</b>\n"
            f"📉 Índice: {data['value']}\n"
            f"🧠 {data['value_classification']}",
            parse_mode="HTML"
        )
    except Exception as e:
        bot.send_message(msg.chat.id, "⚠️ Erro ao buscar Fear & Greed")
        print("ERRO FEAR:", repr(e))

# ================= TOP =================

@bot.message_handler(commands=['top'])
def top(msg):
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/coins/markets"
            "?vs_currency=usd&order=market_cap_desc&per_page=5&page=1",
            headers=HEADERS,
            timeout=10
        )
        coins = r.json()
        text = "🏆 <b>TOP MOEDAS</b>\n\n"
        for c in coins:
            text += f"🔹 <b>{c['name']} ({c['symbol'].upper()})</b>\n💰 ${c['current_price']:,.2f}\n\n"
        bot.send_message(msg.chat.id, text, parse_mode="HTML")
    except Exception as e:
        bot.send_message(msg.chat.id, "⚠️ Erro ao buscar TOP moedas")
        print("ERRO TOP:", repr(e))

# ================= ROMPIMENTOS =================
@bot.message_handler(commands=['rompimentos'])
def rompimentos(msg):
    bot.send_message(msg.chat.id, "🔍 Analisando possíveis rompimentos...")
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/coins/markets"
            "?vs_currency=usd&order=volume_desc&per_page=20&page=1",
            headers=HEADERS,
            timeout=10
        )

        coins = r.json()
        text = "🚀 <b>POSSÍVEIS ROMPIMENTOS</b>\n<i>Volume + variação 24h</i>\n\n"
        encontrados = 0

        for c in coins:
            change = c.get("price_change_percentage_24h")
            if change is not None and change >= 8:
                encontrados += 1
                text += (
                    f"🔥 <b>{c['name']} ({c['symbol'].upper()})</b>\n"
                    f"📈 {change:.2f}% | 💰 ${c['current_price']:,.4f}\n\n"
                )

        if encontrados == 0:
            text += "😴 Nenhum rompimento forte no momento."

        bot.send_message(msg.chat.id, text, parse_mode="HTML")

    except Exception as e:
        bot.send_message(msg.chat.id, "⚠️ Erro ao buscar rompimentos")
        print("ERRO ROMPIMENTOS:", repr(e))

# ================= RUN =================

print("🤖 Bot iniciado com sucesso")
bot.infinity_polling(skip_pending=True)
