import telebot
import time
import schedule
from telebot import types
from checklists import MORNING_CHECKLIST, EVENING_CHECKLIST_NR_1, EVENING_CHECKLIST_NR_2

USER_ID = 368162759
API_TOKEN = '1808720389:AAEPPfTNd6cxnzQ2WI0jb6mDuiItXm8hzuw'

bot = telebot.TeleBot(API_TOKEN)


def morning_checklist(message):
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Выполнено", callback_data="test")
    keyboard.add(callback_button)
    for point in MORNING_CHECKLIST:
        bot.send_message(message.chat.id, point, reply_markup=keyboard)


def evening_checklist_nr_1(message):
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Выполнено", callback_data="test")
    keyboard.add(callback_button)
    for point in EVENING_CHECKLIST_NR_1:
        bot.send_message(message.chat.id, point, reply_markup=keyboard)


def evening_checklist_nr_2(message):
    keyboard = types.InlineKeyboardMarkup()
    callback_button = types.InlineKeyboardButton(text="Выполнено", callback_data="test")
    keyboard.add(callback_button)
    for point in EVENING_CHECKLIST_NR_2:
        bot.send_message(message.chat.id, point, reply_markup=keyboard)


@bot.message_handler(commands=['start'])
def send_alert(message):
    bot.send_message(message.chat.id, 'Bot started')
    schedule.every().day.at("14:20").do(morning_checklist, message)
    schedule.every().day.at("14:21").do(evening_checklist_nr_1, message)
    schedule.every().day.at("14:22").do(evening_checklist_nr_2, message)
    while True:
        schedule.run_pending()
        time.sleep(1)


# В большинстве случаев целесообразно разбить этот хэндлер на несколько маленьких
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    user_first_name = call.from_user.first_name
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='~' + call.message.text + '~' + "\n Изменил — " + user_first_name, parse_mode='MarkdownV2')


bot.polling(none_stop=True, interval=0)
