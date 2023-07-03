# -*- coding: utf-8 -*-
# Bot management system for promoting accounts on instagram #

__author__ = 'Konstantin Bychkov <inco.k.b.blizz@gmail.com>'
__copyright__ = 'Copyright 2023, RLT IP.'
__version__ = '0.1.2'

import json
import time
import datetime
from pprint import pprint
import openai
import selenium.webdriver.chrome.options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from b_scripts.HAR import *
from b_scripts.RD import remove_duplicates
from b_scripts.TN import time_normalization
from b_scripts.RIS import randomize_input_stream


def add_user(name: str, main_link: str) -> None:
    try:
        with open('../c_data/users.json', 'r', encoding='utf-8') as json_file:
            json_data: dict = json.load(json_file)
            for item in json_data.items():
                if item[0] == name:
                    print("Имя занято")
                    return None
    except Exception as json_ex:
        print(f"Ошибка при работе с json \n {json_ex}")

    try:
        with open('../c_data/bots.json', 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)
            username = json_data['main_bot']['username']
            password = json_data['main_bot']['password']
    except Exception as json_ex:
        print(f"Ошибка при работе с json \n {json_ex}")

    try:
        options = selenium.webdriver.chrome.options.ChromiumOptions()
        options.add_argument("--start-maximized")
        browser = webdriver.Chrome(options=options)
        browser.get('https://www.instagram.com')
    except Exception as browser_ex:
        print(f"Ошибка при работе с драйвером \n {browser_ex}")

    have_a_rest(4)

    try:
        username_input = browser.find_element(By.NAME, "username")
        username_input.clear()
        username_input.send_keys(username)
    except Exception as input_username_ex:
        print(f"Ошибка при работе записи в поле username \n {input_username_ex}")

    have_a_rest(1)

    try:
        password_input = browser.find_element(By.NAME, "password")
        password_input.clear()
        password_input.send_keys(password)
        have_a_rest(2)
        password_input.send_keys(Keys.ENTER)
    except Exception as input_password_ex:
        print(f"Ошибка при работе записи в поле password или ошибка при входе \n {input_password_ex}")

    have_a_rest(5)

    browser.get(main_link)

    have_a_rest(4)

    try:
        count_post = browser.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[1]/span/span").text
        count_post = int(count_post) // 12
    except Exception as find_count_post:
        print(f"Ошибка при получение количества постов \n {find_count_post}")
    have_a_rest(4)

    try:
        all_links = []
        for _ in range(count_post):
            hrefs = browser.find_elements(By.TAG_NAME, 'a')
            current_links = [item.get_attribute('href') for item in hrefs if '/p/' in item.get_attribute('href')]
            all_links += current_links
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            have_a_rest(1)
        all_links = remove_duplicates(all_links)
    except Exception as links_ex:
        print(f"Ошибка при получение ссылок \n {links_ex}")

    have_a_rest(2)

    try:
        with open('../c_data/users.json', 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)
            json_data[name] = {
                "main_link": main_link,
                "post_links": all_links
            }
            with open('../c_data/users.json', 'w', encoding='utf-8') as copy_json_file:
                json.dump(json_data, copy_json_file, ensure_ascii=False, indent=4)
    except Exception as json_ex:
        print(f"Ошибка при работе с json \n {json_ex}")

    browser.close()
    browser.quit()


def add_bot(name: str, username: str, password: str) -> None:
    try:
        with open('../c_data/bots.json', 'r', encoding='utf-8') as json_file:
            json_data: dict = json.load(json_file)
            for item in json_data.items():
                if item[0] == name:
                    print("Имя занято")
                    return None
    except Exception as json_ex:
        print(f"Ошибка при работе с json \n {json_ex}")

    try:
        with open('../c_data/bots.json', 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)
            json_data[name] = {
                "username": username,
                "password": password,
                "users": [

                ]
            }
            with open('../c_data/bots.json', 'w', encoding='utf-8') as copy_json_file:
                json.dump(json_data, copy_json_file, ensure_ascii=False, indent=4)
    except Exception as json_ex:
        print(f"Ошибка при работе с json \n {json_ex}")


def start():
    # 6:00 - 9:00 12:00 - 14:00 17:30 - 22:00
    timing = randomize_input_stream()
    print(*timing)

    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")
        timing = randomize_input_stream() if time_normalization(current_time) == '00:00' else timing


def pre_rate(bot_name: str) -> None:
    def rate(bot_username: str, bot_password: str, user: str, links: list) -> None:
        with open('../c_data/users.json', 'r', encoding='utf-8') as _json_file:
            _json_data: dict = json.load(_json_file)
            all_links = _json_data[user]['post_links']
        for _ in all_links:
            if not (_ in links):
                # Поставить Боту bot_name лайк по ссылке _
                try:
                    options = selenium.webdriver.chrome.options.ChromiumOptions()
                    options.add_argument("--start-maximized")
                    browser = webdriver.Chrome(options=options)
                    browser.get('https://www.instagram.com')
                except Exception as browser_ex:
                    print(f"Ошибка при работе с драйвером \n {browser_ex}")

                have_a_rest(4)

                try:
                    username_input = browser.find_element(By.NAME, "username")
                    username_input.clear()
                    username_input.send_keys(bot_username)
                except Exception as input_username_ex:
                    print(f"Ошибка при работе записи в поле username \n {input_username_ex}")

                have_a_rest(1)

                try:
                    password_input = browser.find_element(By.NAME, "password")
                    password_input.clear()
                    password_input.send_keys(bot_password)
                    have_a_rest(2)
                    password_input.send_keys(Keys.ENTER)
                except Exception as input_password_ex:
                    print(f"Ошибка при работе записи в поле password или ошибка при входе \n {input_password_ex}")

                have_a_rest(5)

                browser.get(_)

                have_a_rest(5)

                like_button = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[1]/span[1]/div')
                like_button.click()

                have_a_rest(2)
                # "/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/div/div/canvas"
                browser.close()
                browser.quit()
                # like_button = browser.find_element(By.XPATH, '')
                like_button = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[3]/div[1]/div[1]/span[2]/div/div')
                like_button = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/section/div/form/div/textarea')
                like_button = browser.find_element(By.XPATH, '')
                like_button = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[1]/header/div[2]/div[1]/div[2]/button/div/div')
                like_button = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[3]/div[1]/div[1]/span[1]/div/div')
                like_button.click()
                '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/section/div/form/div/textarea'
                '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[3]/div[1]/div[3]/div/div/div/div'
    with open('../c_data/bots.json', 'r', encoding='utf-8') as json_file:
        json_data: dict = json.load(json_file)
        username = json_data[bot_name]['username']
        password = json_data[bot_name]['password']

    for items in json_data[bot_name]['users'].items():
        rate(bot_username=username, bot_password=password, user=items[0], links=items[1])



def get_response(
        req: str = "create five comments similar to the following:\nU litt bruddah🔥\nShieeed that’s fye gang💯\nKeep it up broski\nYessuhhhhh\nU killed dat ho💯💯\nDa Realest💯\nI fw it✊🏻\nOk ok I see u gang🔒\nStraight up brodie🔥\nAyeeee🔥🔥\n"
) -> dict:
    openai.api_key = "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"
    a = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": req}
        ]
    )
    return json.loads(str(a))['choices'][0]['message']['content']


if __name__ == "__main__":
    start()


# like = browser.fin"/html/body/div[2]/div/div/div[3]/div/div/div[1]/div/div[3]/div/div/div/div/div[2]/div/article/div/div[2]/div/div/div[2]/section[1]/span[1]/div"
# d_element(By.XPATH, '').click()
# import json
# from random import randint
# from time import sleep as slp
#
# from b_scripts.TN import time_normalization
# from multiprocessing import process
#
#
# def randomize_input_stream():
#     try:
#         with open('c_data/bots.json', 'r', encoding='utf-8') as json_file:
#             json_data: dict = json.load(json_file)
#     except Exception as json_ex:
#         print(f"Ошибка при работе с json \n {json_ex}")
#
#     return [
#         [
#             _[0],
#             time_normalization(f"{randint(6, 8)}:{randint(0, 59)}"),
#             time_normalization(f"{randint(12, 13)}:{randint(0, 59)}"),
#             time_normalization(f"{randint(17, 21)}:{randint(0, 59)}"),
#         ]
#         for _ in json_data.items()
#     ]
# def time(time=[0, 0]):
#     if time[1] + 1 == 60:
#         if time[0] + 1 == 24:
#             time[0], time[1] = 0, 0
#         else:
#             time[0] += 1
#             time[1] = 0
#     else:
#         time[1] += 1
#     return time[0], time[1]
#
#
# class Manager:
#     def __init__(self):
#         ...
#
#     def add_bot(self, name: str, username: str, password: str):
#         print("Открываю botjson")
#         print("записываю нового бота")
#         print("Сохраняю файл", '\n', "="*100)
#
#     def add_user(self, name: str, main_link: str):
#         print("Беру данные главного бота")
#         print("Захожу в инсту, копирую все ссылки постов пользователя")
#         print("Открываю userjson")
#         print("записываю нового пользователя")
#         print("Сохраняю файл")
#         print(f"Обновляю счетчик на клиента {name}", '\n', "="*100)
#
#     def start(self):
#         print("Рандомизирую время активности ботов по 3 интервалам")
#         timing = randomize_input_stream()
#         print(timing, '\n', "="*100)
#         while True:
#             h, m = time()
#             current_time = time_normalization(f"{h}:{m}")
#             if current_time == "00:00":
#                 print("Наступил новый день")
#                 print("Рандомизирую время активности ботов по 3 интервалам")
#                 timing = randomize_input_stream()
#                 print(timing, '\n', "="*100)
#
#             # print("cверяю время с временем активности")
#             for bots in timing:
#                 if current_time == bots[1] or current_time == bots[2] or current_time == bots[3]:
#                     print(f"Есть совпадение (Бот >>> {bots[0]} time >>> {current_time})", '\n', "="*100)
#                     with open('c_data/bots.json', 'r', encoding='utf-8') as BotsJson:
#                         BotsData: dict = json.load(BotsJson)
#                     for i in BotsData[bots[0]]['users'].items():
#                         with open('c_data/users.json', 'r', encoding='utf-8') as UsersJson:
#                             UsersData: dict = json.load(UsersJson)
#                             all_links = UsersData[i[0]]['post_links']
#                         for link in all_links:
#                             if not (link in i[1]):
#                                 self.__clicker(bots[0], i[0], BotsData[bots[0]]['username'], BotsData[bots[0]]['password'], link)
#                                 break
#                         else:
#                             # Подписка
#                             ...
#
#                         print(f"Счетчик {i[0]} ++")
#
#                         # if счетчик % 4 or % 5
#                         #   random bot add this person
#
#
#
#             # Если совпало
#             # Если не совпало
#             slp(1/30)
#
#     def __clicker(self, botname, un, username, password, link):
#         print(f"Бот {botname} лайкнул {un}\thref >>> {link}")
#         if randint(0, 10) in range(5):
#             print(f"Бот {botname} закоментил {un}\thref >>> {link}")
#             if randint(0, 10) in range(3):
#                 print(f"Бот {botname} сохранил {un}\thref >>> {link}")
#         print(f"Добавил href={link} человека {un} в botsjson на бота {botname}", '\n', "="*100)
#
#
# if __name__ == '__main__':
#     manager = Manager()
#     manager.start()