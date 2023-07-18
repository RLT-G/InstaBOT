import datetime
import random

def increase_time_randomly(time_str):
    # Преобразуем строку времени в объект datetime
    time_obj = datetime.datetime.strptime(time_str, '%H:%M')

    # Вычисляем случайное количество времени в пределах 1.5 часа
    random_time_delta = datetime.timedelta(hours=random.uniform(0, 1.5))

    # Увеличиваем время на случайный интервал
    increased_time = time_obj + random_time_delta

    # Форматируем результат в строку времени "%H:%M"
    increased_time_str = increased_time.strftime('%H:%M')

    return increased_time_str

# Пример использования
input_time = "00:34"
increased_time = increase_time_randomly(input_time)
print("Увеличенное время:", increased_time)
