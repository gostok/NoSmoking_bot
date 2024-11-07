from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


about_message = (
    'NSB - No Smoking Bot\n\n'
    'Python==3.12, aiogram==3.10.0.\n'
    'Created by gostok.'
)


def kb_about():
    kb_list = [
        [InlineKeyboardButton(text="Донат", callback_data="donat_donat")],
        [InlineKeyboardButton(text="Другие проекты", url="https://github.com/gostok?tab=repositories")],
        [InlineKeyboardButton(text="Сотрудничать", url="https://t.me/ateccc")]
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=kb_list, resize_keyboard=True)
    return kb