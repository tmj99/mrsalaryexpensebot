import os
import telebot

BOT_TOKEN = os.environ.get('BOT_TOKEN')
BOT_ADMIN_ID = os.environ.get('MREXPENSE_ADMIN')

for key, value in os.environ.items():
    print(f"{key}: {value}")

bot = telebot.TeleBot(BOT_TOKEN)

class IsAdmin(telebot.custom_filters.SimpleCustomFilter):
    key='is_admin'
    @staticmethod
    def check(message: telebot.types.Message):
        return message.from_user.id == int(BOT_ADMIN_ID)

bot.add_custom_filter(IsAdmin())

@bot.message_handler(is_admin=True,commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Time to track some expenses")

@bot.message_handler(is_admin=True, func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.infinity_polling()