import telebot
import requests
import os
import time

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
    text = (
        "🤖 <b>SATOSHIDOFEBOT ONLINE</b>\n\n"
        "📊 Monitoramento do mercado cripto em tempo real\n\n"
        "⚔️ <b>Comandos iniciais:</b>\n"
        "/btc - Preço do Bitcoin\n"
        "/eth - Preço do Ethereum\n"
        "/dominance - Dominância do BTC\n"
        "/fear - Fear & Greed Index\n"
        "/top - Top moedas do dia\n"
        "/rompimentos - Possíveis rompimentos\n"
        "/ajuda - Lista completa\n"
    )
    bot.send_message(msg.chat.id, text, parse_mode="HTML")

# ================= AJUDA =================

@bot.message_handler(commands=['ajuda'])
def ajuda(msg):
    bot.send_message(
        msg.chat.id,
        "🧭 <b>AJUDA</b>\n\n"
        "/btc - Preço do Bitcoin\n"
        "/eth - Preço do Ethereum\n"
        "/dominance - Dominância do BTC\n"
        "/fear - Sentimento do mercado\n"
        "/top - Top moedas por market cap\n"
        "/rompimentos - Volume + variação\n",
        parse_mode="HTML"
    )

# ================= BTC =================

@bot.message_handler(commands=['btc'])
def btc(msg):
    bot.send_message(msg.chat.id, "🟠 Buscando preço do Bitcoin...")
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd",
            headers=HEADERS,
            timeout=10
        )
        if r.status_code != 200:
            raise Exception("CoinGecko bloqueou")
        price = r.json()["bitcoin"]["usd"]
        bot.send_message(msg.chat.id, f"🟠 <b>BITCOIN (BTC)</b>\n💰 ${price:,.2f}", parse_mode="HTML")
    except Exception as e:
        bot.send_message(msg.chat.id, "⚠️ Erro ao buscar BTC")
        print("ERRO BTC:", repr(e))

# ================= ETH =================

@bot.message_handler(commands=['eth'])
def eth(msg):
    bot.send_message(msg.chat.id, "🔵 Buscando preço do Ethereum...")
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd",
            headers=HEADERS,
            timeout=10
        )
        if r.status_code != 200:
            raise Exception("CoinGecko bloqueou")
        price = r.json()["ethereum"]["usd"]
        bot.send_message(msg.chat.id, f"🔵 <b>ETHEREUM (ETH)</b>\n💰 ${price:,.2f}", parse_mode="HTML")
    except Exception as e:
        bot.send_message(msg.chat.id, "⚠️ Erro ao buscar ETH")
        print("ERRO ETH:", repr(e))

# ================= DOMINANCE =================

@bot.message_handler(commands=['dominance'])
def dominance(msg):
    bot.send_message(msg.chat.id, "📊 Buscando dominância do BTC...")
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/global",
            headers=HEADERS,
            timeout=10
        )
        btc_dom = r.json()["data"]["market_cap_percentage"]["btc"]
        bot.send_message(msg.chat.id, f"📊 <b>DOMINÂNCIA DO BITCOIN</b>\n🟠 BTC: {btc_dom:.2f}%", parse_mode="HTML")
    except Exception as e:
        bot.send_message(msg.chat.id, "⚠️ Erro ao buscar dominância")
        print("ERRO DOM:", repr(e))

# ================= FEAR & GREED =================

@bot.message_handler(commands=['fear'])
def fear(msg):
    bot.send_message(msg.chat.id, "😱 Buscando Fear & Greed Index...")
    try:
        r = requests.get("https://api.alternative.me/fng/", timeout=10)
        data = r.json()["data"][0]
        bot.send_message(
            msg.chat.id,
            f"😱 <b>FEAR & GREED INDEX</b>\n📉 Índice: {data['value']}\n🧠 Sentimento: {data['value_classification']}",
            parse_mode="HTML"
        )
    except Exception as e:
        bot.send_message(msg.chat.id, "⚠️ Erro ao buscar Fear & Greed")
        print("ERRO FEAR:", repr(e))# ================= TOP MOEDAS =================

@bot.message_handler(commands=['top'])
def top(msg):
    bot.send_message(msg.chat.id, "🏆 Buscando TOP moedas do dia...")
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/coins/markets"
            "?vs_currency=usd&order=market_cap_desc&per_page=5&page=1",
            headers=HEADERS,
            timeout=10
        )

        if r.status_code != 200:
            bot.send_message(msg.chat.id, "⚠️ CoinGecko limitou requisições. Tente depois.")
            print("TOP STATUS:", r.status_code)
            return

        coins = r.json()
        text = "🏆 <b>TOP MOEDAS DO DIA</b>\n\n"

        for c in coins:
            text += (
                f"🔹 <b>{c['name']} ({c['symbol'].upper()})</b>\n"
                f"💰 ${c['current_price']:,.2f}\n\n"
            )

        bot.send_message(msg.chat.id, text, parse_mode="HTML")

    except Exception as e:
        bot.send_message(msg.chat.id, "⚠️ Erro ao buscar TOP moedas")
        print("ERRO TOP:", repr(e))

# ================= ROMPIMENTOS (À PROVA DE FALHA) =================

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

        if r.status_code != 200:
            bot.send_message(msg.chat.id, "⚠️ CoinGecko bloqueou temporariamente")
            return

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
