from aiogram import Router, F, types
import asyncio
import logging

from base.booking import *
from routers.donat_router.donat_kb import *




donat_router = Router()

@donat_router.callback_query(F.data.startswith("donat_donat"))
async def donat_in(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer("Меню Доната:", reply_markup=donat_kb())

