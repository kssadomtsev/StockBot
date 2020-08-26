import configparser
from bot import keyboards
from utils import utils

from telegram.ext.dispatcher import run_async

logger = utils.get_logger()

# Read config data
config = configparser.ConfigParser()
config.read("config.ini")

buffer_chat = config['Logic']['buffer_chat']
special_sender = config['Logic']['special_sender']


@run_async
def media(update, context):
    logger.info("Now working media handler that handle messages from regular users")
    message = update.message
    logger.info(str(message))
    logger.info("Now let's determine is it message from special user or not")
    user = update.message.from_user
    if user.username == special_sender:
        logger.info("It is special user " + special_sender)
        caption = message.caption
        keyboard = keyboards.media_bot_message_kb()
    else:
        logger.info("It is regular user " + str(user.username))
        caption = "#предложка"
        keyboard = keyboards.media_message_kb(user)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Спасибо за предложенный контент, " + update.effective_user.username)
    logger.info("Let's determine what type of media user send")
    if message.photo:
        logger.info("This is photo. Now resending it to buffer chat")
        utils.send_photo(message=message, context=context, caption=caption,
                         keyboard=keyboard, chat_id=buffer_chat)
    elif message.video:
        logger.info("This is video. Now resending it to buffer chat")
        utils.send_video(message=message, context=context, caption=caption,
                         keyboard=keyboard, chat_id=buffer_chat)
    elif message.document:
        logger.info("This is gif. Now resending it to buffer chat")
        utils.send_document(message=message, context=context, caption=caption,
                            keyboard=keyboard, chat_id=buffer_chat)
    else:
        logger.info("Unknown media type")