import logging

from telegram.ext.dispatcher import run_async


def get_logger():
    logger = logging.getLogger()
    logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    return logger


@run_async
def invalid_command(update, context):
    text = "Несуществующая команда"
    update.message.reply_text(text=text, quote=True)


@run_async
def send_photo(message, context, caption, keyboard, chat_id):
    media = message.photo[-1].file_id
    context.bot.send_photo(chat_id=chat_id, photo=media, caption=caption, reply_markup=keyboard)


@run_async
def send_video(message, context, caption, keyboard, chat_id):
    media = message.video.file_id
    duration = message.video.duration
    context.bot.send_video(chat_id=chat_id, video=media, duration=duration, caption=caption, reply_markup=keyboard)


@run_async
def send_document(message, context, caption, keyboard, chat_id):
    media = message.document.file_id
    filename = message.document.file_name
    context.bot.send_document(chat_id=chat_id, document=media, filename=filename, caption=caption, reply_markup=keyboard)