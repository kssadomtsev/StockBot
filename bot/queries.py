import configparser
from telegram.ext.dispatcher import run_async

from utils import utils

logger = utils.get_logger()

# Read config data
config = configparser.ConfigParser()
config.read("config.ini")

public = config['Logic']['public']

@run_async
def delete_button(update, context):
    logger.info("Delete button handler")
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    context.bot.deleteMessage(chat_id=update.effective_chat.id, message_id=query.message.message_id)


@run_async
def send_button(update, context):
    logger.info("Send button handler")
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    logger.info("Get message..")
    message = query.message
    logger.info(str(message))
    logger.info("Let's determine what type of media")
    if message.photo:
        logger.info("This is photo. Now resending it to public")
        utils.send_photo(message=message, context=context, caption=message.caption,
                         keyboard=None, chat_id="@"+public)
    elif message.video:
        logger.info("This is video. Now resending it to public")
        utils.send_video(message=message, context=context, caption=message.caption,
                         keyboard=None, chat_id="@"+public)
    elif message.document:
        logger.info("This is gif. Now resending it to public")
        utils.send_document(message=message, context=context, caption=message.caption,
                         keyboard=None, chat_id="@"+public)
    else:
        logger.info("Unknown media type")
    context.bot.deleteMessage(chat_id=update.effective_chat.id, message_id=query.message.message_id)