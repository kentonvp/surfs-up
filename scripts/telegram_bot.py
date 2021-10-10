import os
import telebot
import threading

from surfsup.comm.message_builder import MessageBuilder


"""Main"""
my_secret = os.environ['TELEGRAM_KEY']
bot = telebot.TeleBot(my_secret)
messenger = MessageBuilder()


@bot.message_handler(commands=["setup"])
def collect_user_preferences(message):
    bot.send_message(message.chat.id, "Changing your User Preferences?")


@bot.message_handler(commands=["Hello"])
def greet(message):
    bot.send_message(message.chat.id, "Hey! Are you ready to shred?")


@bot.message_handler(func=lambda message: messenger.is_spot(message.text))
def report(message):
    msg = messenger.build_report_message(message.text)
    bot.send_message(message.chat.id, msg)


def run_bot():
    bot.polling()


t = threading.Thread(target=run_bot)
t.start()

print("SurfsUp-Bot is started on a thread")