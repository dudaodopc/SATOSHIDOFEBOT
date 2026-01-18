import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🚀 *Bem-vindo ao SATOSHI TERMINAL*\n\n"
        "📊 Dados em tempo real da Binance\n"
        "📈 Gráficos automáticos\n"
        "🔔 Alertas de preço e rompimentos\n"
        "🤖 Interpretação inteligente de mercado\n\n"
        "👉 Use comandos como:\n"
        "`/BTC`   /ETH  `/SOL`\n"
        "`/TOP`  `/ALERT`\n\n"
        "_Powered by FETRADER_"
    )

    await update.message.reply_text(
        text,
        parse_mode="Markdown"
    )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
