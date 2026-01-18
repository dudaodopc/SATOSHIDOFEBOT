import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg, "🤖 SATOSHIDOFEBOT está online!")

print("Bot iniciado...")
bot.infinity_polling()
