import configparser
from bot import keyboards
from utils import utils

from telegram import (ParseMode, ReplyKeyboardRemove)

from telegram.ext import (ConversationHandler)
from telegram.ext.dispatcher import run_async

logger = utils.get_logger()

MESSAGE = range(1)

# Read config data
config = configparser.ConfigParser()
config.read("config.ini")

buffer_chat = config['Logic']['buffer_chat']


@run_async
def help_command(update, context):
    keyboard = keyboards.channel_link_kb()
    text = (
        "<b>Это предложка-бот канала <a href='https://t.me/savedmemess'>Сохранёнки</a> - картинки на все случаи жизни. </b>\n\n"
        "С помощью меня ты можешь предложить админу канала картинку, видео, альбом или гифку,"
        " а также оставить сообщение.\n\n"
        "<b>Поддерживаемые команды:</b>\n"
        "/start <i>Начало работы с ботом</i>\n"
        "/help <i>Справка</i>\n"
        "/message <i>Отправить сообщение админу канала</i>\n\n"
        "<b><i>Чтобы предложить картинку, видео, альбом или гифку просто перешли контент боту</i></b>"
    )
    update.message.reply_text(text=text, parse_mode=ParseMode.HTML, reply_markup=keyboard)


def message_command(update, context):
    user = update.message.from_user
    logger.info("User %s initiate conversation to send message to admin", user.username)
    update.message.reply_text("Просто отправь текст сообщения или "
                              "введи команду /cancel если передумал отправлять сообщение.")
    return MESSAGE


def send_message_to_admin(update, context):
    user = update.message.from_user
    message = update.message
    logger.info("User %s send following text message to admin %s", user.username, message.text)
    update.message.reply_text("Спасибо! Твоё сообщение будет доставлено админу")
    keyboard = keyboards.text_message_kb(user)
    context.bot.send_message(chat_id=buffer_chat,
                             text="<b>Пользователь " + user.username + " прислал сообщение через форму обратной связи:</b>\n\n" + message.text,
                             parse_mode=ParseMode.HTML,
                             reply_markup=keyboard)
    return ConversationHandler.END


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.username)
    update.message.reply_text('Ты отменил отправку сообщения админу. До скорого!',
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def timeout(update, context):
    user = update.message.from_user
    logger.info("User %s timeout is expired", user.username)
    update.message.reply_text('Таймаут на отправку сообщения истёк')