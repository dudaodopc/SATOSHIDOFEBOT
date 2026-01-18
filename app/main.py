import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from app.binance import get_ticker

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 *SATOSHI TERMINAL ONLINE*\n\n"
        "Digite o símbolo da moeda:\n"
        "`/BTC` /ETH `/SOL`\n\n"
        "_Dados direto da Binance_",
        parse_mode="Markdown"
    )

async def crypto_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    symbol = update.message.text.replace("/", "").upper()
    data = get_ticker(symbol)

    if not data:
        await update.message.reply_text("❌ Moeda não encontrada na Binance.")
        return

    message = (
        f"📊 *{symbol}/USDT*\n\n"
        f"💰 Preço: `${data['price']:,.2f}`\n"
        f"📈 Variação 24h: `{data['change']:.2f}%`\n"
        f"💧 Volume 24h: `${data['volume']:,.0f}`\n\n"
        "_Fonte: Binance_"
    )

    await update.message.reply_text(message, parse_mode="Markdown")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler(None, crypto_command))

    app.run_polling()

if __name__ == "__main__":
    main()
