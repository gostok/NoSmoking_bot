from aiogram import Router, F, types
import asyncio
import logging
from datetime import datetime, timedelta
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter

from base.booking import *
from base.database import *
from routers.first_menu_router.first_menu_kb import *
from routers.first_menu_router.first_menu_booking import *
from routers.first_menu_router.timer import *

first_menu_router = Router()

@first_menu_router.message(F.text.startswith("Вернуться назад"))
async def back_kb(message: types.Message):
    await message.answer('Вы вернулись назад.', reply_markup=first_menu_kb())

@first_menu_router.message(F.text.startswith("About"))
async def about_kb_f(message: types.Message):
    await message.answer(about_message, reply_markup=kb_about())

@first_menu_router.message(F.text.startswith("План"))
async def plan_f(message: types.Message):
    await message.answer(plan_f_message, reply_markup=first_menu_kb())




class TimerState(StatesGroup):
    start_time_state = State()
    end_time_state = State()

@first_menu_router.message(F.text.startswith("Сброс"))
async def reset_timer_f(message: types.Message):
    await message.answer('Выберите действие:', reply_markup=kb_reset())

@first_menu_router.message(F.text.startswith("Начать с начала"))
async def restart_timer_f(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(timer_start_message, reply_markup=prodoljit())
    await state.set_state(TimerState.start_time_state)

@first_menu_router.message(F.text.startswith("Отключить таймер"))
async def disable_timer_f(message: types.Message):
    global current_timer
    if current_timer:
        current_timer.cancel()
    await message.answer("Таймер отключен. Вы можете включить его позже, когда будете готовы.")

async def notify_user():
    global start_time, end_time, current_day
    cigarettes_per_day, times_per_day = smoking_schedule[current_day]
    interval_hours = (end_time - start_time).total_seconds() / (times_per_day * 3600)

    current_time = start_time

    while current_time < end_time:
        await asyncio.sleep(interval_hours * 3600)  # Ждать до следующего уведомления
        if current_time < end_time:
            # Уведомление пользователю
            await first_menu_router.bot.send_message(chat_id, f"Пора курить! Время: {current_time.strftime('%H:%M')}")
        current_time += timedelta(hours=interval_hours)


@first_menu_router.message(F.text.startswith("Продолжить"), StateFilter(TimerState.start_time_state))
async def set_time_f(message: types.Message, state: FSMContext):
    global chat_id
    chat_id = message.chat.id
    await message.answer("Выберите временной интервал курения:", reply_markup=kb_inteval_time())
    await message.answer('__________________________________________', reply_markup=kb_back())
    await state.set_state(TimerState.end_time_state)

@first_menu_router.callback_query(F.data.startswith("time_interval_"), StateFilter(TimerState.end_time_state))
async def receive_interval_time_f(callback: types.CallbackQuery, state: FSMContext):
    global start_time, end_time
    interval = callback.data.split('_')[2]
    start_hour, end_hour = interval.split('-')

    start_time = datetime.strptime(start_hour, "%H:%M").replace(year=datetime.now().year, month=datetime.now().month,
                                                                day=datetime.now().day)
    end_time = datetime.strptime(end_hour, "%H:%M").replace(year=datetime.now().year, month=datetime.now().month,
                                                            day=datetime.now().day)

    user_id = callback.from_user.id
    add_timer(user_id, start_time.isoformat(), end_time.isoformat(), (end_time - start_time).seconds // 3600)


    await callback.answer()  # Удаляем уведомление
    await callback.message.answer("Таймер установлен! Бот начнет уведомлять вас о времени курения.",
                                  reply_markup=kb_reset())

    global current_timer
    if current_timer:
        current_timer.cancel()  # Остановить текущий таймер, если он есть
    current_timer = asyncio.create_task(notify_user())
    await state.clear()


@first_menu_router.message(F.text.startswith("⏳ Когда курить?"))
async def when_to_smoke_fm(message: types.Message):
    try:
        user_id = message.from_user.id
        timer = get_timer(user_id)

        if not timer:
            await message.answer('Вы не установили таймер.\n\nВоспользуйтесь кнопкой "Сброс" в меню.')
            return

        start_time = datetime.strptime(timer[2], '%Y-%m-%dT%H:%M:%S')
        end_time = datetime.strptime(timer[3], '%Y-%m-%dT%H:%M:%S')
        interval_hours = timer[4]

        current_time = datetime.now().replace(second=0, microsecond=0)

        next_smoke_time = start_time
        while next_smoke_time <= current_time:
            next_smoke_time += timedelta(hours=interval_hours)

        if next_smoke_time > end_time:
            await message.answer("Все запланированные времена курения на сегодня уже прошли.")
            return

        time_until_next_smoke = next_smoke_time - current_time
        hours, remainder = divmod(time_until_next_smoke.total_seconds(), 3600)
        minutes, _ = divmod(remainder, 60)

        response_message = f"Следующее время курения: {next_smoke_time.strftime('%H:%M')}. " \
                           f"Осталось времени: {int(hours)} ч {int(minutes)} мин."
        await message.answer(response_message)

    except Exception as e:
        logging.error(f"Ошибка в обработчике when_to_smoke_fm: {e}")
        await message.answer('Произошла ошибка. Попробуйте снова.')
