from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter

from routers.main_menu_router.main_menu_kb import *
from routers.main_menu_router.main_menu_booking import *
from routers.first_menu_router.first_menu_kb import first_menu_kb
from routers.second_menu_router.second_menu_kb import second_menu_kb
from base.booking import kb_about, about_message
from routers.start_router.start import start_kb
from base.database import register_user, update_user_plan

main_menu = Router()

class RegistrationStates(StatesGroup):
    waiting_for_plan = State()
    waiting_for_confirmation = State()




@main_menu.message(F.text.startswith("Начать регистрацию"))
async def login_kb(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(reg_1_message, reply_markup=kb_confirm())
    await state.set_state(RegistrationStates.waiting_for_confirmation)


@main_menu.message(F.text.startswith("Подтвердить"), StateFilter(RegistrationStates.waiting_for_confirmation))
async def confirm_reg(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username if message.from_user.username else "Не указан"

    register_user(user_id, username)

    await message.answer(f"Регистрация завершена!\nЗдравствуй, {message.from_user.full_name}.\n\n" + reg_2_message, reply_markup=kb_plan())

    await state.set_state(RegistrationStates.waiting_for_plan)

@main_menu.message(F.text.startswith("1. Бросить курить"), StateFilter(RegistrationStates.waiting_for_plan))
async def plan_reg(message: types.Message, state: FSMContext):
    update_user_plan(message.from_user.id, "Бросить курить")

    await message.answer(plan_1_message, reply_markup=first_menu_kb())
    await state.clear()


@main_menu.message(F.text.startswith("2. Таймер курения"), StateFilter(RegistrationStates.waiting_for_plan))
async def plan_reg(message: types.Message, state: FSMContext):
    update_user_plan(message.from_user.id, "Таймер курения")

    await message.answer(plan_2_message, reply_markup=second_menu_kb())
    await state.clear()
