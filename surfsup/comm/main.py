import json
import os

import telebot
from surfsup.surfline.api import SurflineAPI
from surfsup.utils import joinpath

surfline = SurflineAPI(joinpath('data', 'spot_lookups.csv'))

my_secret = os.environ['TELEGRAM_KEY']
bot = telebot.TeleBot(my_secret)


def is_spot(spot_name: str) -> bool:
    """Return if message text indicates a spot name."""
    return spot_name in list(surfline.database.table['name'])


def clean(obj: dict) -> str:
    value = obj['conditions']['value']
    surf_min = obj['waveHeight']['min']
    surf_max = obj['waveHeight']['max']
    surf_rel = obj['waveHeight']['humanRelation']
    return f'Surf Report: {value}\nSurf is {surf_min}ft to {surf_max}ft and is {surf_rel.lower()}.\nHave fun!'


def build_report_message(spot_name: str) -> str:
    spot_url = surfline.build_spot_url(spot_name)
    report_data = surfline.spot_check(spot_url)
    new_message = clean(report_data['forecast'])
    return new_message




@bot.message_handler(commands=["setup"])
def collect_user_preferences(message):
    bot.send_message(message.chat.id, "Changing your User Preferences?")


@bot.message_handler(commands=["Hello"])
def greet(message):
    bot.send_message(message.chat.id, "Hey! Are you ready to shred?")


@bot.message_handler(func=lambda message: is_spot(message.text))
def report(message):
    msg = build_report_message(message.text)
    bot.send_message(message.chat.id, msg)


bot.polling()

# pyTelegramBotAPI package
