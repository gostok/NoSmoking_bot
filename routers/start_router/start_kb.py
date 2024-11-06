from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def start_kb():
    kb_list = [
        [KeyboardButton(text="Войти"), KeyboardButton(text="Зарегистрироваться")],
        [KeyboardButton(text="About")]
    ]
    kb = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True)
    return kb