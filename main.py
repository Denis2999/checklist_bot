import telebot
import time
import schedule

USER_ID = id
API_TOKEN = 'token'

bot = telebot.TeleBot(API_TOKEN)


def morning_checklist(message):
    bot.send_message(message.chat.id, "I'm working... at morning")


def evening_checklist(message):
    bot.send_message(message.chat.id, "I'm working... at evening")


@bot.message_handler(commands=['start'])
def send_alert(message):
    schedule.every().day.at("18:13").do(morning_checklist, message)
    schedule.every().day.at("18:15").do(morning_checklist, message)
    print("OK")
    while True:
        schedule.run_pending()
        time.sleep(1)


bot.polling(none_stop=True, interval=0)
