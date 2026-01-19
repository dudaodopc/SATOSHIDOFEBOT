import telebot
import os
import requests

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise Exception("BOT_TOKEN não encontrado")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# ================= START =================
@bot.message_handler(commands=['start', 'ajuda'])
def start(msg):
    bot.send_message(
        msg.chat.id,
        "🤖 <b>SATOSHIDOFEBOT ONLINE</b>\n\n"
        "<b>Comandos disponíveis:</b>\n"
        "/btc — Preço do Bitcoin\n"
        "/eth — Preço do Ethereum\n"
        "/top — Top moedas do dia\n"
        "/rompimentos — Possíveis rompimentos\n"
        "/dominance — Dominância do BTC\n"
        "/fear — Fear & Greed Index"
    )

# ================= BTC =================
@bot.message_handler(commands=['btc'])
def btc(msg):
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        price = requests.get(url, headers=HEADERS, timeout=10).json()["bitcoin"]["usd"]

        bot.send_message(
            msg.chat.id,
            f"🟠 <b>BITCOIN (BTC)</b>\n💰 Preço: <b>${price:,.2f}</b>\nFonte: CoinGecko"
        )
    except Exception as e:
        bot.send_message(msg.chat.id, "⚠️ Erro ao buscar BTC")
        print("BTC:", e)

# ================= ETH =================
@bot.message_handler(commands=['eth'])
def eth(msg):
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
        price = requests.get(url, headers=HEADERS, timeout=10).json()["ethereum"]["usd"]

        bot.send_message(
            msg.chat.id,
            f"🔵 <b>ETHEREUM (ETH)</b>\n💰 Preço: <b>${price:,.2f}</b>\nFonte: CoinGecko"
        )
    except Exception as e:
        bot.send_message(msg.chat.id, "⚠️ Erro ao buscar ETH")
        print("ETH:", e)

# ================= FEAR & GREED =================
@bot.message_handler(commands=['fear'])
def fear(msg):
    try:
        url = "https://api.alternative.me/fng/"
        data = requests.get(url, timeout=10).json()["data"][0]

        bot.send_message(
            msg.chat.id,
            "😱 <b>FEAR & GREED INDEX</b>\n"
            f"📊 Índice: <b>{data['value']}</b>\n"
            f"🧠 Sentimento: <b>{data['value_classification']}</b>"
        )
    except Exception as e:
        bot.send_message(msg.chat.id, "⚠️ Erro ao buscar Fear & Greed")
        print("FEAR:", e)

# ================= DOMINANCE =================
@bot.message_handler(commands=['dominance'])
def dominance(msg):
    try:
        url = "https://api.coingecko.com/api/v3/global"
        btc_dom = requests.get(url, headers=HEADERS, timeout=10).json()["data"]["market_cap_percentage"]["btc"]

        bot.send_message(
            msg.chat.id,
            f"📊 <b>DOMINÂNCIA DO BITCOIN</b>\n🟠 BTC: <b>{btc_dom:.2f}%</b>"
        )
    except Exception as e:
        bot.send_message(msg.chat.id, "⚠️ Erro ao buscar dominância")
        print("DOMINANCE:", e)

# ================= TOP MOEDAS =================
@bot.message_handler(commands=['top'])
def top(msg):
    try:
        url = (
            "https://api.coingecko.com/api/v3/coins/markets"
            "?vs_currency=usd&order=market_cap_desc&per_page=5&page=1"
        )
        coins = requests.get(url, headers=HEADERS, timeout=10).json()

        text = "🏆 <b>TOP MOEDAS DO DIA</b>\n\n"
        for c in coins:
            text += (
                f"🔹 <b>{c['name']} ({c['symbol'].upper()})</b>\n"
                f"💰 ${c['current_price']:,.2f}\n\n"
            )

        bot.send_message(msg.chat.id, text)
    except Exception as e:
        bot.send_message(msg.chat.id, "⚠️ Erro ao buscar TOP moedas")
        print("TOP:", e)# ================= ROMPIMENTOS (CORRIGIDO) =================
@bot.message_handler(commands=['rompimentos'])
def rompimentos(msg):
    try:
        url = (
            "https://api.coingecko.com/api/v3/coins/markets"
            "?vs_currency=usd&order=volume_desc&per_page=20&page=1"
        )
        coins = requests.get(url, headers=HEADERS, timeout=10).json()

        text = "🚀 <b>POSSÍVEIS ROMPIMENTOS</b>\n<i>Volume + Variação 24h</i>\n\n"
        count = 0

        for c in coins:
            change = c.get("price_change_percentage_24h")
            if change and change >= 8:
                count += 1
                text += (
                    f"🔥 <b>{c['name']} ({c['symbol'].upper()})</b>\n"
                    f"📈 +{change:.2f}%\n"
                    f"💰 ${c['current_price']:,.4f}\n\n"
                )

            if count >= 7:  # 🔒 limite seguro
                break

        if count == 0:
            text += "⚠️ Nenhum rompimento forte agora."

        bot.send_message(msg.chat.id, text)
    except Exception as e:
        bot.send_message(msg.chat.id, "⚠️ Erro ao buscar rompimentos")
        print("ROMPIMENTOS:", e)

# ================= RUN =================
print("🤖 Bot iniciado com sucesso")
bot.infinity_polling(skip_pending=True)

