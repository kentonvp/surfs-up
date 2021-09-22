import os
import telebot

my_secret = os.environ['API_KEY']
bot = telebot.TeleBot(my_secret)

@bot.message_handler(commands=["Hello"])
def greet(message):
  bot.send_message(message.chat.id, "Hey! Are you ready to shred?")

bot.polling()

#pyTelegramBotAPI package
