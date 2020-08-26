import configparser
from telegram import (InputMediaPhoto, ChatAction, ParseMode)

from utils import utils

ALBUM_DICT = {}

logger = utils.get_logger()

# Read config data
config = configparser.ConfigParser()
config.read("config.ini")

buffer_chat = config['Logic']['buffer_chat']


def collect_album_items(update, context):
    """
    if the media_group_id not a key in the dictionary yet:
        - send sending action
        - create a key in the dict with media_group_id
        - add a list to the key and the first element is this update
        - schedule a job in 1 sec
    else:
        - add update to the list of that media_group_id
    """
    logger.info("Now working media handler that handle messages with album from regular users")
    message = update.message
    logger.info(str(message))
    media_group_id = update.message.media_group_id
    if media_group_id not in ALBUM_DICT:
        context.bot.sendChatAction(chat_id=update.message.from_user.id, action=ChatAction.UPLOAD_PHOTO)
        ALBUM_DICT[media_group_id] = [update]
        # schedule the job
        context.job_queue.run_once(send_album, 1, context=[media_group_id])
    else:
        ALBUM_DICT[media_group_id].append(update)


def send_album(context):
    media_group_id = context.job.context[0]
    updates = ALBUM_DICT[media_group_id]

    # delete from ALBUM_DICT
    del ALBUM_DICT[media_group_id]

    # ordering album updates
    updates.sort(key=lambda x: x.message.message_id)

    media = []
    for update in updates:
        media.append(InputMediaPhoto(media=update.message.photo[-1].file_id))
    context.bot.sendMessage(chat_id=buffer_chat, text="<b>#предложка в виде альбома от пользователя @"
                                                      + updates[0].message.from_user.username+"\nПерешли альбом боту, "
                                                      "если хочешь запостить</b>", parse_mode=ParseMode.HTML)
    context.bot.sendMediaGroup(chat_id=buffer_chat, media=media)
    context.bot.sendMessage(chat_id=updates[0].message.from_user.id, text="Спасибо за альбом, " + updates[0].message.from_user.username)
