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
To enter a new expense, use the /spent command!""")

@bot.message_handler(is_admin=True,commands=['spent'])
def spent(message):
    response_message = bot.reply_to(message,"How much did you spend?")
    bot.register_next_step_handler(response_message, spent_collect_cost)
    
def spent_collect_cost(message):
    msg_input_cost = message.text
    try:
        response_message_cost = bot.reply_to(message,"What did you spend £{} on?".format(msg_input_cost))
        bot.register_next_step_handler(response_message_cost, spent_collect_desc)
    except:
        error_message = bot.reply_to(message,"You entered {}. Please enter a real number.".format(msg_input_cost))
        bot.register_next_step_handler(error_message,spent_collect_cost)

def spent_collect_desc(message):
    try:
        # global msg_input_desc
        msg_input_desc = message.text
        response_message_desc = bot.reply_to(message,"You spent on {}. Is this correct? (y/n)".format(msg_input_desc))
        bot.register_next_step_handler(response_message_desc, spent_collect_confirm)
    except:
        bot.reply_to(message,"Oops, something went wrong")

def spent_collect_confirm(message):
    while True:
        try:
            msg_input = message.text
            if msg_input == str("y"):
                bot.reply_to(message,"Perfect! Expenditure noted.")
                break
            elif msg_input == str("n"):
                bot.reply_to(message,"Let's try again then.")
                break
            else:
                break
        except:
            bot.reply_to(message,"Please enter 'y' or 'n'.")

# message_strung = message.text.split(";",1)
# expense_cost = message_strung[0]
# expense_item = message_strung[1]
# bot.reply_to(message, """You just {} on {}""".format(expense_cost, expense_item))

bot.enable_save_next_step_handlers()

bot.load_next_step_handlers()

bot.infinity_polling()
