# NSB: No Smoking Bot

## Описание:

Это Телеграм бот, который поможет либо бросить курить, либо систематизировать курение, используя таймер.

## Функционал:

- система регистрации пользователя;
- таймер курения;
- уведомления от бота пользователю, когда можно курить, учитывая временной интервал, например с 8:00 до 20:00 каждые 2 часа;
- бд для хранения информации о пользователе, таймера и выбранного плана (их два, с разной логикой).

## Инструменты:
- Python 3.12
- Aiogram 3.10.0
- datetime
- sqlite3

### Установка:

git clone https://github.com/gostok/NoSmoking_bot.git <br>
cd NoSmoking_bot <br>
pip install -r requirements.txt

### Запуск:

py run_bot.py