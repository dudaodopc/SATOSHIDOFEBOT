print("ERRO TOP:", repr(e))

# ================= ROMPIMENTOS (À PROVA DE FALHA) =================
@bot.message_handler(commands=['rompimentos'])
def rompimentos(msg):
    bot.send_message(msg.chat.id, "🔍 Analisando possíveis rompimentos...")

    try:
        url = (
            "https://api.coingecko.com/api/v3/coins/markets"
            "?vs_currency=usd&order=volume_desc&per_page=25&page=1"
        )

        coins = requests.get(url, headers=HEADERS, timeout=10).json()

        text = "🚀 <b>POSSÍVEIS ROMPIMENTOS</b>\n<i>Volume + variação 24h</i>\n\n"
        encontrados = 0

        for c in coins:
            change = c.get("price_change_percentage_24h")
            if change is None:
                continue

            if change >= 8:
                encontrados += 1
                text += (
                    f"🔥 <b>{c['name']} ({c['symbol'].upper()})</b>\n"
                    f"📈 +{change:.2f}%\n"
                    f"💰 ${c['current_price']:,.4f}\n\n"
                )

            if encontrados == 5:
                break

        if encontrados == 0:
            text += "⚠️ Nenhum rompimento forte detectado agora."

        bot.send_message(msg.chat.id, text)

    except Exception as e:
        bot.send_message(msg.chat.id, "⚠️ Erro ao buscar rompimentos")
        print("ERRO ROMPIMENTOS:", repr(e))

# ================= RUN =================
print("🤖 Bot iniciado com sucesso")
bot.infinity_polling(skip_pending=True)

