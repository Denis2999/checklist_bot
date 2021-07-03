import telebot
import time
import schedule
from telebot import types
from checklists import MORNING_CHECKLIST, EVENING_CHECKLIST

USER_ID = 368162759
API_TOKEN = '1808720389:AAEPPfTNd6cxnzQ2WI0jb6mDuiItXm8hzuw'

bot = telebot.TeleBot(API_TOKEN)


def morning_checklist(message):
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Выполнено", callback_data="test")
    keyboard.add(callback_button)
    for point in MORNING_CHECKLIST:
        bot.send_message(message.chat.id, point, reply_markup=keyboard)


def evening_checklist(message):
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Выполнено", callback_data="test")
    keyboard.add(callback_button)
    for point in EVENING_CHECKLIST:
        bot.send_message(message.chat.id, point, reply_markup=keyboard)


@bot.message_handler(commands=['start'])
def send_alert(message):
    schedule.every().day.at("13:54").do(morning_checklist, message)
    schedule.every().day.at("13:55").do(evening_checklist, message)
    print("Bot started...")
    while True:
        schedule.run_pending()
        time.sleep(1)


# В большинстве случаев целесообразно разбить этот хэндлер на несколько маленьких
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    user_first_name = call.from_user.first_name
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='~' + call.message.text + '~' + "\n Changed by " + user_first_name, parse_mode='MarkdownV2')


bot.polling(none_stop=True, interval=0)
