from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery



def main_menu_kb():
    kb_list = [
        [KeyboardButton(text="Начать регистрацию")],
        [KeyboardButton(text="Вернуться назад")]
    ]
    kb = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)
    return kb



def kb_confirm():
    kb_list = [
        [KeyboardButton(text="Подтвердить")],
        [KeyboardButton(text="Вернуться назад")]
    ]
    kb = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=False)
    return kb

def kb_plan():
    kb_list = [
        [KeyboardButton(text="1. Бросить курить")],
        [KeyboardButton(text="2. Таймер курения")],
        [KeyboardButton(text="Вернуться назад")]
    ]
    kb = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True)
    return kb