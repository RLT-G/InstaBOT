import json
from b_scripts.TN import time_normalization
from random import randint


def randomize_input_stream():
    try:
        with open('../c_data/bots.json', 'r', encoding='utf-8') as json_file:
            json_data: dict = json.load(json_file)
    except Exception as json_ex:
        print(f"Ошибка при работе с json \n {json_ex}")

    return [
        [
            _[0],
            time_normalization(f"{randint(6, 8)}:{randint(0, 59)}"),
            time_normalization(f"{randint(12, 13)}:{randint(0, 59)}"),
            time_normalization(f"{randint(17, 21)}:{randint(0, 59)}"),
        ]
        for _ in json_data.items()
    ]
