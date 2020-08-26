import os
import sys
import configparser

from telegram.ext import (Updater, CommandHandler, MessageHandler, ConversationHandler, CallbackQueryHandler, Filters)
from utils import utils
from bot import commands, queries, messages, filters, albums

CHAT_TIMEOUT = 60

logger = utils.get_logger()

# Read system variables
mode = os.getenv("MODE")
TOKEN = os.getenv("TOKEN")

# Read config data
config = configparser.ConfigParser()
config.read("config.ini")

bot_user_name = config['Bot']['bot_user_name']
URL = config['Bot']['URL']
port = int(config['Bot']['port'])
special_sender = config['Logic']['special_sender']

if mode == "dev":
    def run(updater):
        logger.info("Dev mode select")
        updater.start_polling()
elif mode == "prod":
    def run(updater):
        logger.info("Prod mode select")
        # Code from https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#heroku
        updater.start_webhook(listen="0.0.0.0",
                              port=port,
                              url_path=TOKEN)
        updater.bot.set_webhook("{URL}{HOOK}".format(URL=URL, HOOK=TOKEN))
else:
    logger.error("No MODE specified!")
    sys.exit(1)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    logger.info("Starting bot")
    # define the updater
    updater = Updater(TOKEN, use_context=True)

    # define the dispatcher
    dp = updater.dispatcher

    # define jobs
    j = updater.job_queue

    # commands
    dp.add_handler(CommandHandler(('start', 'help'), commands.help_command))
    # conversation send message to admin
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('message', commands.message_command)],

        states={
            commands.MESSAGE: [MessageHandler(Filters.text & ~Filters.command, commands.send_message_to_admin)],
            ConversationHandler.TIMEOUT: [MessageHandler(Filters.text | Filters.command, commands.timeout)]

        },

        fallbacks=[CommandHandler('cancel', commands.cancel)],
        conversation_timeout=CHAT_TIMEOUT
    )
    dp.add_handler(conv_handler)
    # All unrecognized commands
    dp.add_handler(MessageHandler(Filters.command, utils.invalid_command))

    # callbacks
    dp.add_handler(CallbackQueryHandler(queries.delete_button, pattern=r'del'))
    dp.add_handler(CallbackQueryHandler(queries.send_button, pattern=r'send'))

    # Initialize custom filters
    filter_album = filters.FilterAlbum()

    # messages
    # Messages with photo, videos, gif and not album from users
    media_handler = MessageHandler((Filters.video | Filters.photo | Filters.document.mime_type(
        "video/mp4")) & ~ filter_album & ~ Filters.update.channel_posts, messages.media)
    dp.add_handler(media_handler)

    # Album with photos from users
    media_album_handler = MessageHandler(
        filter_album & Filters.photo & ~ Filters.update.channel_posts & ~ Filters.user(username=special_sender),
        albums.collect_album_items)
    dp.add_handler(media_album_handler)

    # handle errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
