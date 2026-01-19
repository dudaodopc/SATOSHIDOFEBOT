import telebot
import requests
import os
import time
from dotenv import load_dotenv

# ===================== ENV =====================
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise Exception("❌ BOT_TOKEN não encontrado nas variáveis de ambiente")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# ===================== START =====================
@bot.message_handler(commands=["start"])
def start(msg):
    bot.send_message(
        msg.chat.id,
        "🤖 <b>SATOSHIDOFEBOT ONLINE</b>\n\n"
        "📊 Monitoramento do mercado cripto em tempo real\n\n"
        "⚔️ <b>Comandos iniciais:</b>\n"
        "/btc - Preço do Bitcoin\n"
        "/eth - Preço do Ethereum\n"
        "/dominance - Dominância do BTC\n"
        "/fear - Fear & Greed Index\n"
        "/top - Top moedas do dia\n"
        "/rompimentos - Possíveis rompimentos\n"
        "/ajuda - Lista completa"
    )

# ===================== AJUDA =====================
@bot.message_handler(commands=["ajuda"])
def ajuda(msg):
    bot.send_message(
        msg.chat.id,
        "🧭 <b>AJUDA</b>\n\n"
        "/btc - Preço do Bitcoin\n"
        "/eth - Preço do Ethereum\n"
        "/dominance - Dominância do BTC\n"
        "/fear - Sentimento do mercado\n"
        "/top - Top moedas por market cap\n"
        "/rompimentos - Moedas em possível rompimento"
    )

# ===================== BTC =====================
@bot.message_handler(commands=["btc"])
def btc(msg):
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd",
            headers=HEADERS,
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
        bot.send_message(msg.chat.id, "⚠️ Erro ao buscar BTC")
        print("ERRO BTC:", repr(e))

# ===================== ETH =====================
@bot.message_handler(commands=["eth"])
def eth(msg):
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd",
            headers=HEADERS,
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
        bot.send_message(msg.chat.id, "⚠️ Erro ao buscar ETH")
        print("ERRO ETH:", repr(e))

# ===================== DOMINANCE =====================
@bot.message_handler(commands=["dominance"])
def dominance(msg):
    try:
        r = requests.get(
            "https://api.coingecko.com/api/v3/global",
            headers=HEADERS,
            timeout=10
        )
        r.raise_for_status()
        btc_dom = r.json()["data"]["market_cap_percentage"]["btc"]

        bot.send_message(
            msg.chat.id,
            f"📊 <b>DOMINÂNCIA DO BITCOIN</b>\n\n"
            f"🟠 BTC: <b>{btc_dom:.2f}%</b>"
        )
    except Exception as e:
        bot.send_message(msg.chat.id, "⚠️ Erro ao buscar dominância")
        print("ERRO DOMINANCE:", repr(e))

# ===================== FEAR & GREED =====================
@bot.message_handler(commands=["fear"])
def fear(msg):
    try:
        r = requests.get(
            "https://api.alternative.me/fng/",
            timeout=10
        )
        r.raise_for_status()
        data = r.json()["data"][0]

        bot.send_message(
            msg.chat.id,
            "😱 <b>FEAR & GREED INDEX</b>\n\n"
            f"📉 Índice: <b>{data['value']}</b>\n"
            f"🧠 Sentimento: <b>{data['value_classification']}</b>"
        )
    except Exception as e:
        bot.send_message(msg.chat.id, "⚠️ Erro ao buscar Fear & Greed")
        print("ERRO FEAR:", repr(e))# ===================== TOP MOEDAS =====================
@bot.message_handler(commands=["top"])
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
                f"🔹 <b>{c['name']}</b> ({c['symbol'].upper()})\n"
                f"💰 ${c['current_price']:,.2f}\n\n"
            )

        bot.send_message(msg.chat.id, text)
    except Exception as e:
        bot.send_message(msg.chat.id, "⚠️ Erro ao buscar TOP moedas")
        print("ERRO TOP:", repr(e))

# ===================== ROMPIMENTOS (À PROVA DE FALHA) =====================
@bot.message_handler(commands=["rompimentos"])
def rompimentos(msg):
    bot.send_message(msg.chat.id, "🔍 Analisando possíveis rompimentos...")

    try:
        url = (
            "https://api.coingecko.com/api/v3/coins/markets"
            "?vs_currency=usd&order=volume_desc&per_page=25&page=1"
        )
        r = requests.get(url, headers=HEADERS, timeout=10)

        if r.status_code != 200:
            bot.send_message(msg.chat.id, "⚠️ CoinGecko indisponível no momento")
            return

        coins = r.json()
        encontrados = 0

        text = "🚀 <b>POSSÍVEIS ROMPIMENTOS</b>\n<i>Volume + variação 24h</i>\n\n"

        for c in coins:
            change = c.get("price_change_percentage_24h")
            if change is not None and change >= 8:
                encontrados += 1
                text += (
                    f"🔥 <b>{c['name']}</b> ({c['symbol'].upper()})\n"
                    f"📈 {change:.2f}% | 💰 ${c['current_price']:,.4f}\n\n"
                )

        if encontrados == 0:
            text += "😴 Nenhum rompimento forte no momento."

        bot.send_message(msg.chat.id, text)

    except Exception as e:
        bot.send_message(msg.chat.id, "⚠️ Erro ao buscar rompimentos")
        print("ERRO ROMPIMENTOS:", repr(e))

# ===================== RUN (NUNCA DUPLICAR) =====================
print("🤖 Bot iniciado com sucesso")

while True:
    try:
        bot.infinity_polling(skip_pending=True)
    except Exception as e:
        print("ERRO GERAL:", repr(e))
        time.sleep(5)
