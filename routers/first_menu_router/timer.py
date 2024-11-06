


current_timer = None
start_time = None
end_time = None
interval_hours = None
chat_id = None
current_day = 1  # Начальный день в схеме курения

# Схема курения
smoking_schedule = {
    1: (8, 2),  # 1-3 день: 8 раз в день, каждые 2 часа
    2: (8, 2),
    3: (8, 2),
    4: (6, 2.5),  # 4-12 день: 6 раз в день, каждые 2.5 часа
    5: (6, 2.5),
    6: (6, 2.5),
    7: (6, 2.5),
    8: (6, 2.5),
    9: (6, 2.5),
    10: (6, 2.5),
    11: (6, 2.5),
    12: (6, 2.5),
    13: (5, 3),  # 13-16 день: 5 раз в день, каждые 3 часа
    14: (5, 3),
    15: (5, 3),
    16: (5, 3),
    17: (4, 5),  # 17-20 день: 4 раза в день, каждые 5 часов
    18: (4, 5),
    19: (4, 5),
    20: (4, 5),
    21: (1, 24),  # 21-25 день: 1-2 сигареты в день
    22: (1, 24),
    23: (1, 24),
    24: (1, 24),
    25: (1, 24),
}


