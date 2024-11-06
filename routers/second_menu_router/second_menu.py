from aiogram import Router, F, types
import asyncio
import logging
from datetime import datetime, timedelta
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter

from base.booking import *
from base.database import *
from routers.second_menu_router.second_menu_kb import *
from routers.second_menu_router.second_menu_booking import *
from routers.second_menu_router.timer import *
from routers.main_menu_router.main_menu_kb import kb_plan

second_menu_router = Router()


@second_menu_router.message(F.text.startswith("Вернуться назад"))
async def back_kb(message: types.Message):
    await message.answer('Вы вернулись назад.', reply_markup=second_menu_kb())

@second_menu_router.message(F.text.startswith("About"))
async def about_kb_s(message: types.Message):
    await message.answer(about_message, reply_markup=kb_about())



class TimerState_S(StatesGroup):
    select_interval_state = State()
    smoking_interval_state = State()
    when_to_smoke_s_state = State()


async def notify_user(start_time, end_time, interval_hours):
    current_time = start_time

    while current_time < end_time:
        await asyncio.sleep(interval_hours * 3600)  # Ждать до следующего уведомления
        if current_time < end_time:
            # Уведомление пользователю
            await second_menu_router.bot.send_message(chat_id, f"Пора курить! Время: {current_time.strftime('%H:%M')}")
        current_time += timedelta(hours=interval_hours)


@second_menu_router.message(F.text.startswith("Таймер"))
async def reset_timer_s(message: types.Message):
    await message.answer('Выберите действие:', reply_markup=kb_res_s())

@second_menu_router.message(F.text.startswith("Отключить ⏰"))
async def disable_timer_f(message: types.Message, state: FSMContext):
    await state.clear()
    global current_timer
    user_id = message.from_user.id

    if current_timer:
        current_timer.cancel()
    delete_timer(user_id)

    await message.answer("Таймер отключен. Вы можете включить его позже, когда будете готовы.")

@second_menu_router.message(F.text.startswith("⏰ Новый таймер"))
async def restart_timer_s(message: types.Message, state: FSMContext):

    await message.answer(timer_restart_message, reply_markup=kb_inteval_s())
    await state.set_state(TimerState_S.select_interval_state)

@second_menu_router.callback_query(F.data.startswith("time_interval_"), StateFilter(TimerState_S.select_interval_state))
async def receive_time_interval_s(callback: types.CallbackQuery, state: FSMContext):
    interval = callback.data.split('_')[2]
    start_hour, end_hour = interval.split('-')

    start_time = datetime.strptime(start_hour, "%H:%M").replace(year=datetime.now().year, month=datetime.now().month,
                                                                day=datetime.now().day)
    end_time = datetime.strptime(end_hour, "%H:%M").replace(year=datetime.now().year, month=datetime.now().month,
                                                            day=datetime.now().day)

    await callback.answer()
    await callback.message.answer(smoking_interval_message, reply_markup=kb_smoking_intervals())
    await state.set_state(TimerState_S.smoking_interval_state)

    await state.update_data(start_time=start_time, end_time=end_time)

@second_menu_router.callback_query(F.data.startswith("interval_"), StateFilter(TimerState_S.smoking_interval_state))
async def receive_smoking_interval_s(callback: types.CallbackQuery, state: FSMContext):
    interval_mapping = {
        "interval_1": 1,
        "interval_2": 2,
        "interval_3": 3,
        "interval_4": 4,
        "interval_5": 5,
        "interval_6": 6,
        "interval_24": 24,
    }

    interval_hours = interval_mapping[callback.data]

    await callback.answer()
    await callback.message.answer("Таймер установлен!\nБот начнет уведомлять вас, когда можно курить.",
                                  reply_markup=second_menu_kb())

    data = await state.get_data()
    start_time = data.get("start_time").isoformat()
    end_time = data.get("end_time").isoformat()
    user_id = callback.from_user.id

    add_timer(user_id, start_time, end_time, interval_hours)

    global current_timer
    if current_timer:
        current_timer.cancel()  # Остановить текущий таймер, если он есть
    current_timer = asyncio.create_task(notify_user(start_time, end_time, interval_hours))
    await state.clear()


@second_menu_router.message(F.text.startswith("⌚ Когда курить?"))
async def when_to_smoke_sm(message: types.Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        timer = get_timer(user_id)

        if not timer:
            await message.answer('Вы не установили таймер.\n\nВоспользуйтесь кнопкой "Таймер" в меню.')
            return

        start_time = timer[2]
        end_time = timer[3]
        interval_hours = timer[4]

        start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S')
        end_time = datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S')

        now = datetime.now()

        next_smoke_time = start_time
        while next_smoke_time <= now:
            next_smoke_time += timedelta(hours=interval_hours)

        time_until_next_smoke = next_smoke_time - now

        hours, remainder = divmod(time_until_next_smoke.total_seconds(), 3600)
        minutes, _ = divmod(remainder, 60)

        await message.answer(f"Следующее время для курения: {next_smoke_time.strftime('%H:%M')}\n"
                             f"Осталось: {int(hours)} ч {int(minutes)} мин.")
    except Exception as e:
        logging.error(f"Ошибка в обработчике when_to_smoke_sm: {e}")
        await message.answer('Произошла ошибка. Попробуйте снова.')