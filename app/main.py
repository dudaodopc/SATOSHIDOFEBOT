
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from aplicativo.binance import get_price

TOKEN = os.getenv("BOT_TOKEN")

async def btc(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price = get_price("BTCUSDT")
    await update.message.reply_text(f"📈 BTC agora: ${price}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("BTC", btc))
    app.run_polling()

if __name__ == "__main__":
    main()
