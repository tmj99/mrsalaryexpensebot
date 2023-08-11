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
    bot.reply_to(message, """Hello! Let me help you track your expenses!
    To enter a new expense, use the spent command with the following format:
    /spent _amount_;_description_
    """)

@bot.message_handler(is_admin=True,commands=['spent'])
def spent(message):
    message_strung = message.text.split(";",1)
    expense_cost = message_strung[0]
    expense_item = message_strung[1]
    bot.reply_to(message, """You just {} on {}""".format(expense_cost, expense_item))

bot.infinity_polling()