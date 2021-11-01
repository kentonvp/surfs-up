import os
import traceback
import telebot
import json
import threading

from surfsup.comm.message_builder import MessageBuilder
from surfsup.maps import Location
from surfsup.user import ShortboardPreferences, User, Activity, export_users, read_users

user_information: dict[int, User] = read_users('user_information.json')
tmp_storage = {}


def give_tmp_storage(uid):
    if uid not in tmp_storage:
        tmp_storage[uid] = {}


"""Main"""
my_secret = os.environ['TELEGRAM_KEY']
bot = telebot.TeleBot(my_secret)
messenger = MessageBuilder()


@bot.message_handler(commands=['start'])
def on_start(message):
    msg = "Welcome to SurfsUp_Bot, I am here to help connect YOU to surf " + \
        "spots that fit YOUR surfing. To get started send me the " + \
        "message '/setup', if you need any help text me '/help'"
    bot.send_message(message.chat.id, msg)


@bot.message_handler(commands=['help'])
def help_message(message):
    msg = "Commands -- start with '/' and are one word. List of currently implemented:" + \
        "\n  /help -- You know this one already" + \
        "\n  /setup -- This helps you setup your preferences for an activity" + \
        "\n  /activity -- Select your activity and see what is currently set" + \
        "\n\nSpot Check -- send me the name of a spot and I'll give you a brief summary of it's current report" + \
        "\n\nPin Drop -- send me a location and I'll give you a list of the top 5 spots based on YOUR preferences"
        # "\n  /creator -- Little 'c' creator" + \

    bot.reply_to(message, msg)


@bot.message_handler(commands=['creator'])
def creater_message(message):
    msg = "The name's Kenton. I'm an ocean lover. My primary activity of choice" + \
        " is shortboarding, but I also love taking out the log or twinny, running on the beach" + \
        " with my wife, or just setting up a chair and opening a good book." + \
        "\n\nProblem: Whatever activity I was feeling on a particular day," + \
        " I'd have to search through my favorite spots and try and find the" + \
        " best conditions for that activity. For example sorting by size and" + \
        " good winds when shortboarding, maybe smaller surf for when I wanted" + \
        " a cruisier day on the log, or maybe a drained tide if my wife" + \
        " wanted to go for a run on the beach... So also being a programmer I" + \
        " decied to automate it." + \
        "\n\bSolution: SurfsUp_Bot is an interactive bot which can store different" + \
        " custom preferences based on activity. These preferences are then used" + \
        "to filter and sort surf reports, giving you the best spots for your activity." + \
        "\n\nI hope this is can be used as a tool to streamline the difficult decision" + \
        " of deciding which beach to go to." + \
        " Thanks for reading, now get out there and remember to have fun!"
    bot.reply_to(message, msg)


@bot.message_handler(commands=['activity'])
def select_activity(message):
    give_tmp_storage(message.chat.id)
    if message.chat.id in user_information:
        msg = bot.reply_to(message,
                           f"Current activity: {user_information[message.chat.id].current_activity()}" +
                           f"\nDo you want to change it?")
        bot.register_next_step_handler(msg, parse_set_activity_handler)
    else:
        tmp_storage[message.chat.id] = {}
        msg = bot.reply_to(message,
                           "You currenly don't have any activities setup, would you like to do that now?")
        bot.register_next_step_handler(msg, parse_set_user_preferences_handler)


def parse_set_activity_handler(message):
    if message.text.lower() == 'yes':
        msg = bot.reply_to(message, 'Select activity:\n(1) Shortboarding')
        bot.register_next_step_handler(msg, parse_activity_handler)
    else:
        bot.reply_to(
            message, 'Alright. When you want to edit your current activity, send /activity!')


def parse_activity_handler(message):
    try:
        if message.text.lower() in ['1', 'shortboarding']:
            bot.reply_to(
                message, "Okay shredder, you're activity is set to shortboarding! [insert tip]")
        else:
            msg = bot.reply_to(message, "Sorry, that wasn't one of the options. " +
                               'Please try again, the options are:\n' +
                               "(1) Shortboarding")
            bot.register_next_step_handler(msg, parse_activity_handler)
    except Exception as exc:
        trace = traceback.format_exc(limit=1)
        print(trace)
        bot.reply_to(message, "FAILURE")


@bot.message_handler(commands=["setup"])
def collect_user_preferences(message):
    give_tmp_storage(message.chat.id)
    if message.chat.id in user_information:
        user = user_information[message.chat.id]
        msg = bot.reply_to(message,
                           f"Current Activity Preferences:\n{user.get_activity_preferences()}" +
                           f"\nDo you want to change them?")
        bot.register_next_step_handler(msg, parse_set_user_preferences_handler)
    else:
        msg = bot.reply_to(message, "You currently have no preferences set," +
                           " let's set that up.\nFirst off, what is your name?")
        bot.register_next_step_handler(msg, parse_user_name_handler)


def parse_user_name_handler(message):
    try:
        tmp_storage[message.chat.id]['name'] = message.text
        msg = bot.reply_to(message, f"Hello {message.text}! Please reply with " +
                           "the numeric value of the activity you wish to setup:\n" +
                           "(1) Shortboarding")
        bot.register_next_step_handler(msg, parse_user_activity_handler)
    except Exception as exc:
        trace = traceback.format_exc(limit=1)
        print(trace)
        bot.reply_to(message, 'FAILURE')


def parse_user_activity_handler(message):
    try:
        if message.text == '1':
            user_information[message.chat.id] = User(
                tmp_storage[message.chat.id]['name'], Activity.SHORTBOARD)
            msg = bot.reply_to(message, "Awesome! Looks like you love to rip! " +
                               "What is the maximum distance you'd like to travel? (miles)")
            bot.register_next_step_handler(
                msg, parse_shortboard_max_radius_handler)
        else:
            msg = bot.reply_to(message, "Sorry, that wasn't one of the options. " +
                               'Please try again, the options are:\n' +
                               "(1) Shortboarding")
            bot.register_next_step_handler(msg, parse_user_activity_handler)
    except Exception as exc:
        trace = traceback.format_exc(limit=1)
        print(trace)
        bot.reply_to(message, 'FAILURE')


def parse_set_user_preferences_handler(message):
    """If next message is yes then send to parse_user_prefereces_handler"""
    if message.text.lower() == "yes":
        # check if has User already
        if message.chat.id in user_information:
            msg = bot.reply_to(
                message, "What is the maximum distance you'd like to travel? (miles)")
            bot.register_next_step_handler(
                msg, parse_shortboard_max_radius_handler)
        else:
            msg = bot.reply_to(
                message, "First off, what is your name?")
            bot.register_next_step_handler(
                msg, parse_user_name_handler)
    else:
        bot.send_message(
            message.chat.id, "Sounds good! When you wish to, send /setup again!")


def parse_user_preferences_handler(message):
    msg = bot.reply_to(
        message, "What is the maximum distance you'd like to travel? (miles)")
    bot.register_next_step_handler(msg, parse_shortboard_max_radius_handler)


def parse_shortboard_max_radius_handler(message):
    try:
        tmp_storage[message.chat.id]['max_radius'] = int(message.text)

        msg = bot.reply_to(
            message, "What wave height are you most comfortable in? (ft)")
        bot.register_next_step_handler(
            msg, parse_shortboard_wave_height_handler)
    except Exception as exc:
        trace = traceback.format_exc(limit=1)
        print(trace)
        bot.reply_to(message, 'failure')


def parse_shortboard_wave_height_handler(message):
    try:
        preferences = ShortboardPreferences(surf_height=int(
            message.text), travel_distance=tmp_storage[message.chat.id]['max_radius'])
        user_information[message.chat.id].add_activity_preferences(
            Activity.SHORTBOARD, preferences)
        bot.reply_to(message, "You are all set up!")
    except Exception as exc:
        trace = traceback.format_exc(limit=1)
        print(trace)
        bot.reply_to(message, 'FAILURE')


@bot.message_handler(commands=["Hello"])
def greet(message):
    print("The id used is: " + str(message.chat.id))
    bot.send_message(message.chat.id, "Hey! Are you ready to shred?")


@bot.message_handler(content_types=['text'])
def basic_report(message):
    msg = messenger.build_report_message(message.text)
    bot.send_message(message.chat.id, msg)


@bot.message_handler(content_types=['location'])
def location_report(message):
    chat_id = message.chat.id

    pin_location = Location(message.location.latitude,
                            message.location.longitude)
    print(pin_location)
    msg = ''
    if chat_id in user_information:
        user = user_information[chat_id]
        print(f'found user: {user.name}')
        activity_preferences = user.get_activity_preferences()
        if isinstance(activity_preferences, ShortboardPreferences):
            bot.send_message(
                message.chat.id, "Looking for some spots nearest to you!")
            msg = messenger.build_report_message_for_location(
                pin_location,
                activity_preferences.travel_distance,
                activity_preferences.surf_height)
    else:
        print('default user')
        user = user_information[0]
        print(user.to_json())
        activity_preferences = user.get_activity_preferences()
        if isinstance(activity_preferences, ShortboardPreferences):
            bot.send_message(
                message.chat.id, "Looking for some spots nearest to you!")
            msg = messenger.build_report_message_for_location(
                pin_location,
                activity_preferences.travel_distance,
                activity_preferences.surf_height)

    if len(msg) > 0:
        bot.send_message(message.chat.id, msg)


# def run_bot():
try:
    print("SurfsUp-Bot has started")
    bot.polling()
except (Exception, KeyboardInterrupt) as exp:
    trace = traceback.format_exc(limit=1)
    print(trace)

export_users('user_information.json', user_information)
export_users('user_information_backup.json', user_information)


# t = threading.Thread(target=run_bot)
# t.start()


print("SurfsUp-Bot is started on a thread")