import logging
from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery


def donat_kb():
    kb_list = [
        [InlineKeyboardButton(text="Прогресс",
                              web_app=types.WebAppInfo(url="https://www.donationalerts.com/widget/goal/8258259?token=xr92I07pj7TcRDTDGzl9"))],
        [InlineKeyboardButton(text="Задонатить",
                              web_app=types.WebAppInfo(url="https://www.donationalerts.com/r/square_vision_gs"))]
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=kb_list, resize_keyboard=True)
    return kb

