from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def channel_link_kb():
    button0 = InlineKeyboardButton(
        text="Сохранёнки",
        url="https://t.me/savedmemess")
    buttons_list = [[button0]]
    keyboard = InlineKeyboardMarkup(buttons_list)
    return keyboard


def text_message_kb(user):
    keyboard = [[InlineKeyboardButton(text="Удалить", callback_data='del')],
                [InlineKeyboardButton(text="Ответить пользователю в ЛС", url="https://t.me/" + str(user.username))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


def media_message_kb(user):
    keyboard = [[InlineKeyboardButton(text="Удалить", callback_data='del')],
                [InlineKeyboardButton(text="Отправить предложку в паблик", callback_data='send')],
                [InlineKeyboardButton(text="Ответить пользователю в ЛС", url="https://t.me/" + str(user.username))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


def media_bot_message_kb():
    keyboard = [[InlineKeyboardButton(text="Удалить", callback_data='del'),
                InlineKeyboardButton(text="Отправить в паблик", callback_data='send')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup
