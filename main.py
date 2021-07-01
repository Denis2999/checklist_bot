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
    schedule.every().day.at("19:12").do(morning_checklist, message)
    schedule.every().day.at("19:13").do(evening_checklist, message)
    print("Bot started...")
    while True:
        schedule.run_pending()
        time.sleep(1)


# В большинстве случаев целесообразно разбить этот хэндлер на несколько маленьких
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text='\u0336'.join(call.message.text) + '\u0336')

########################################################################################################
@bot.message_handler(commands=['money'])
def start_message(message):
    bot.send_message(message.chat.id, 'Ок, напиши сколько денег в кассе')
    bot.register_next_step_handler(enter_the_money)


def enter_the_money(message):
    bot.reply_to(message, "Денег в кассе: {!s}".format(message.text))


@bot.message_handler(content_types="text")
def any_msg(message):
    bot.send_message(message.chat.id, 'Напиши /money, чтобы ввести количество денег в кассе')


#
# @bot.message_handler(func=lambda message: True)
# def any_message(message):
#     bot.reply_to(message, "Денег в кассе: {!s}".format(message.text))
#
#
# @bot.edited_message_handler(func=lambda message: True)
# def edit_message(message):
#     bot.edit_message_text(chat_id=message.chat.id,
#                           text="Денег в кассе: {!s}".format(message.text),
#                           message_id=message.message_id + 1)


bot.polling(none_stop=True, interval=0)
