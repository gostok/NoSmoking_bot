from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery


from routers.start_router.start_booking import *
from routers.main_menu_router.main_menu_kb import main_menu_kb, kb_plan
from routers.first_menu_router.first_menu_kb import first_menu_kb
from routers.second_menu_router.second_menu_kb import second_menu_kb
from base.booking import *
from routers.start_router.start_kb import *
from base.database import *


start_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(start_message, reply_markup=start_kb())


@start_router.message(F.text.startswith("About"))
async def about_kb_main(message: types.Message):
    await message.answer(about_message, reply_markup=kb_about())

@start_router.message(F.text.startswith("Изменить план"))
async def change_plan(message: types.Message):
    user = get_user(message.from_user.id)
    if user:
        await message.answer('Выберите план:\n\n'
                             '1. Помочь в попытке бросить курить, предоставив план и напоминания;\n'
                             '2. Помочь систематизировать курение, чтобы не больше, не меньше, используя и настраивая таймер.',
                             reply_markup=kb_plan())
    else:
        await message.answer("Пользователь не найден. Пожалуйста, зарегистрируйтесь.")


@start_router.message(F.text.in_(['1. Бросить курить', '2. Таймер курения']))
async def set_new_plan(message: types.Message):
    new_plan = 'Бросить курить' if message.text == '1. Бросить курить' else 'Таймер курения'

    # Обновляем план в базе данных
    update_user_plan(message.from_user.id, new_plan)
    user = get_user(message.from_user.id)
    if user:
        plan = user[3]
        if plan == 'Бросить курить':
            await message.answer(f'Ваш план был успешно изменен на: {new_plan}.', reply_markup=first_menu_kb())
        elif plan == 'Таймер курения':
            await message.answer(f'Ваш план был успешно изменен на: {new_plan}.', reply_markup=second_menu_kb())



@start_router.message(F.text.startswith("Войти"))
async def about_kb_main(message: types.Message):
    user = get_user(message.from_user.id)
    if user:
        plan = user[3]
        if plan == 'Бросить курить':
            await message.answer(f"Вы вошли как {user[2]} с планом: {plan}", reply_markup=first_menu_kb())
        elif plan == 'Таймер курения':
            await message.answer(f"Вы вошли как {user[2]} с планом: {plan}", reply_markup=second_menu_kb())
        else:
            await message.answer('Похоже вы не выбрали план после регистрации.\n'
                                 'Сделайте это, чтобы я понимал, как вам помочь:', reply_markup=kb_plan())

    else:
        await message.answer("Чтобы войти, нужно зарегистрироваться.", reply_markup=start_kb())

@start_router.message(F.text.startswith("Зарегистрироваться"))
async def about_kb_main(message: types.Message):
    user = get_user(message.from_user.id)
    if user:
        await message.answer('Вы уже зарегистрированы.')
    else:
        await message.answer(reg_start_message, reply_markup=main_menu_kb())