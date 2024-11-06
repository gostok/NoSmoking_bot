from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery


def first_menu_kb():
    kb_list = [
        [KeyboardButton(text="⏳ Когда курить?")],
        [KeyboardButton(text="Сброс"), KeyboardButton(text="План")],
        [KeyboardButton(text="Изменить план"), KeyboardButton(text="About")]
    ]
    kb = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True)
    return kb

def kb_reset():
    kb_list = [
        [KeyboardButton(text="Начать с начала"), KeyboardButton(text="Отключить таймер")],
        [KeyboardButton(text="Вернуться назад")]
    ]
    kb = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True)
    return kb

def prodoljit():
    kb_list = [[KeyboardButton(text="Продолжить")], [KeyboardButton(text="Вернуться назад")]]
    kb = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True)
    return kb

def kb_inteval_time():
    kb_list = [
        [InlineKeyboardButton(text="08:00-20:00", callback_data="time_interval_08:00-20:00"),
         InlineKeyboardButton(text="09:00-21:00", callback_data="time_interval_09:00-21:00")],
        [InlineKeyboardButton(text="10:00-22:00", callback_data="time_interval_10:00-22:00"),
         InlineKeyboardButton(text="11:00-23:00", callback_data="time_interval_11:00-23:00")],
        [InlineKeyboardButton(text="12:00-00:00", callback_data="time_interval_12:00-00:00")]
    ]

    kb = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return kb

def kb_back():
    kb_list = [
        [KeyboardButton(text="Вернуться назад")]
    ]
    kb = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True)
    return kb