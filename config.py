import configparser
import os


_conf_path = os.getcwd()+'/config.ini'


class BotConfig:
    def __init__(self):
        self.config = configparser.ConfigParser(delimiters='=')
        self.config.read(_conf_path)
        self.config.sections()

    def get_telegram_id(self):
        token = self.config['telegram']['token']
        print("Telegram id: {}".format(token))
        return token

    def get_wallet(self):
        print("Wallet {}".format(self.config['pool']['wallet']))
        return self.config['pool']['wallet']