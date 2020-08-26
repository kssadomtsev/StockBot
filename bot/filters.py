import configparser

from telegram.ext import BaseFilter

# Read config data
config = configparser.ConfigParser()
config.read("config.ini")

special_sender = config['Logic']['special_sender']


class FilterAlbum(BaseFilter):
    def filter(self, message):
        return message.photo and message.media_group_id is not None


class FilterAdmin(BaseFilter):
    def filter(self, message):
        user = message.from_user.username
        for admin in special_sender.split(','):
            if user.username == admin:
                return True
        return False
