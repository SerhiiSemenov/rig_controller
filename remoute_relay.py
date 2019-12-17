#!/usr/bin/python3

import platform
import telebot
import requests
from config import BotConfig
from threading import Timer


class NullObject(object):
    def __init__(self):
        pass

    def __getattr__(self, item):
        print("relay request {}".format(item))
        return lambda *args, **kwargs: None


def get_relay_obj():
    if platform.machine() == 'armv7l':
        import relay_control
        return relay_control.Relay()
    else:
        return NullObject()


def delayed_start(bot, message, relay):
    relay.relay_on()
    bot.send_message(message.chat.id, 'System start again')


def check_hashrate(bot, message, wallet, relay):
    print("check_hashrate")
    Timer(20 * 60, check_hashrate, [bot, message]).start()
    URL = "https://api.nanopool.org/v1/eth/hashrate/" + wallet
    r = requests.get(url=URL)
    data = r.json()

    print(data['data'])

    if data['data'] < 120:
        bot.send_message(message.chat.id, 'Hash rate is low: {}'.format(data['data']))
    elif data['data'] < 50:
        bot.send_message(message.chat.id, 'Hash rate is critical low: {}'.format(data['data']))
        relay.relay_off()
        bot.send_message(message.chat.id, 'System restart is in process')
        Timer(20, delayed_start, [bot, message]).start()


def main():
    bot_config = BotConfig()
    bot_id = bot_config.get_telegram_id()
    bot = telebot.TeleBot(token=bot_id)
    relay = get_relay_obj()

    @bot.message_handler(commands=['help'])
    def help_message(message):
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
        itembtn1 = telebot.types.KeyboardButton('/start')
        itembtn2 = telebot.types.KeyboardButton('/stop')
        itembtn3 = telebot.types.KeyboardButton('/reset')
        itembtn4 = telebot.types.KeyboardButton('/get_rate')
        markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
        bot.send_message(message.chat.id, "Choose command:", reply_markup=markup)

    @bot.message_handler(commands=['start'])
    def start_command(message):
        relay.relay_on()
        bot.send_message(message.chat.id, 'System start is Ok')
        Timer(10*60, check_hashrate, [bot, message, bot_config.get_wallet(), relay]).start()

    @bot.message_handler(commands=['restart'])
    def restart_command(message):
        relay.relay_off()
        bot.send_message(message.chat.id, 'System restart is in process')
        Timer(20, delayed_start, [bot, message]).start()

    @bot.message_handler(commands=['get_rate'])
    def get_rate_command(message):
        URL = "https://api.nanopool.org/v1/eth/hashrate/" + bot_config.get_wallet()
        r = requests.get(url=URL)
        data = r.json()
        bot.send_message(message.chat.id, 'Hash rate: {}'.format(data['data']))

    @bot.message_handler(commands=['stop'])
    def stop_command(message):
        relay.relay_off()
        bot.send_message(message.chat.id, 'System stopped')

    bot.polling()


if __name__ == "__main__":
    main()
