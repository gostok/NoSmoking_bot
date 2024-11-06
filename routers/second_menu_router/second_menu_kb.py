from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def second_menu_kb():
    kb_list = [
        [KeyboardButton(text="⌚ Когда курить?")],
        [KeyboardButton(text="Таймер"), KeyboardButton(text="Изменить план")],
        [KeyboardButton(text="About")]
    ]
    kb = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True)
    return kb

def kb_res_s():
    kb_list = [
        [KeyboardButton(text="⏰ Новый таймер"), KeyboardButton(text="Отключить ⏰")],
        [KeyboardButton(text="Вернуться назад")]
    ]
    kb = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True)
    return kb

def kb_inteval_s():
    kb_list = [
        [InlineKeyboardButton(text="08:00-20:00", callback_data="time_interval_08:00-20:00"),
         InlineKeyboardButton(text="09:00-21:00", callback_data="time_interval_09:00-21:00")],
        [InlineKeyboardButton(text="10:00-22:00", callback_data="time_interval_10:00-22:00"),
         InlineKeyboardButton(text="11:00-23:00", callback_data="time_interval_11:00-23:00")],
        [InlineKeyboardButton(text="12:00-00:00", callback_data="time_interval_12:00-00:00")]
    ]

    kb = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return kb

def kb_smoking_intervals():
    kb_list = [
        [InlineKeyboardButton(text="1 час", callback_data="interval_1"),
         InlineKeyboardButton(text="2 часа", callback_data="interval_2")],
        [InlineKeyboardButton(text="3 часа", callback_data="interval_3"),
         InlineKeyboardButton(text="4 часа", callback_data="interval_4")],
        [InlineKeyboardButton(text="5 часов", callback_data="interval_5"),
         InlineKeyboardButton(text="6 часов", callback_data="interval_6")],
        [InlineKeyboardButton(text="1 день", callback_data="interval_24")]
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=kb_list)
    return kb
