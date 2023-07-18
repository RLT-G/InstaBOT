__author__ = 'Konstantin Bychkov <inco.k.b.blizz@gmail.com>'
__copyright__ = 'Copyright 2023, RLT IP.'
__version__ = '0.2.8'


from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import selenium.webdriver.chrome.options
from selenium import webdriver


from random import randint, choice, uniform
from multiprocessing import Process, Queue
from time import sleep
import datetime
import json
import sys


class ManagerBase:
    """
    -*- coding: utf-8 -*-
    Bot management system for promoting accounts on instagram
    """
    def __init__(self):
        self.command: dict = self.use_json('d_data/command.json')
        print(f"all commands:\n{self.command.keys()}")

    def add_bot(self, path=None) -> None:
        """
        Method for add bot-data in JSON
        for TXT >>> self.executor(r'self.add_bot(r"C:/Users/Admin/Desktop/User_data.txt")', try_exec=True)
        :param path: file path
        :return: None
        """
        if path is None:
            bot_name, username, password = input("bot-name >>> "), input("username >>> "), input("password >>> ")
            self.use_json(
                path='d_data/bots.json',
                mode='w',
                key=bot_name,
                value={
                    "username": username,
                    "password": password
                }
            )
            print("Successfully added")
        else:
            file = open(path, 'r', encoding='utf-8')
            try:
                txt_data = file.read().split('\n')
                for data in txt_data:
                    current_bot = data.split()
                    self.use_json(
                        path='d_data/bots.json',
                        mode='w',
                        key=current_bot[0],
                        value={
                            "username": current_bot[1],
                            "password": current_bot[2]
                        }
                    )
            except Exception as ex:
                print(ex)
            finally:
                file.close()
                print("Successfully added")

    def add_user(self):
        name, main_links = input('client-name >>> '), input('main-link >>>')
        self.use_json(
            path='d_data/users.json',
            mode='w',
            key=name,
            value={
                "main_links": main_links,
                "signed_bots": []
            }
        )
        print("Successfully added")

    def start(self):
        print('Bot-System launched')
        ...

    def phase_1(self, username: str, password: str, link: str):
        # print(f'phase one has started. data: \nusername - {username}, password - {password}, link - {link}')
        ...

    def phase_2(self):
        ...

    def launch_detector(self):
        ...

    def update_detector(self):
        ...

    def all_c(self):
        print(f"all commands:\n{self.command.keys()}")

    @staticmethod
    def use_json(path: str, mode: str = None, key: str = None, value=None) -> dict | None:
        """
        Method for work with JSON
        :param path: The path to the file
        :param mode: None for read; "w" to write
        :param key: Key for add data in JSON file
        :param value: Value for add data in JSON file
        :return: JSON dict if mode is None else None
        """
        match mode:
            case None:
                try:
                    with open(path, 'r', encoding='utf-8') as json_file:
                        json_data: dict = json.load(json_file)
                    return json_data
                except Exception as ex:
                    print(f"Path error {ex}")
                    return None
            case 'w':
                try:
                    if key is None or value is None:
                        raise ValueError("With the <w> flag, the key and value must be passed")
                    with open(path, 'r', encoding='utf-8') as json_file_r:
                        json_data: dict = json.load(json_file_r)
                        if key in json_data.keys():
                            raise KeyError("The key is busy")
                        json_data[key] = value
                        with open(path, 'w', encoding='utf-8') as json_file_w:
                            json.dump(json_data, json_file_w, ensure_ascii=False, indent=4)
                except Exception as ex:
                    print(ex)
                finally:
                    return None
            case _:
                return None

    def executor(self, command, try_exec: bool = False):
        try:
            exec(command) if try_exec else exec(self.command[command])
        except Exception as ex:
            print(f"Exec error {ex}")

    def run(self):
        while True: 
            command = input(" >>> ")
            if 'try_exec' in command:
                self.executor(command.split()[1], try_exec=True)
            else:
                self.executor(command)


class Manager(ManagerBase):
    def __init__(self):
        super().__init__()
        self.scripts = Scripts()
        self.words = self.use_json("d_data/comments.json")["comments"]
        self.users_data = self.use_json("d_data/users.json")
        self.bots_data = self.use_json("d_data/bots.json")
        self.main_data = self.use_json("d_data/main.json")
        self.input_time = [
            # self.scripts.rtime_from_range("07:00-9:00"), 
            # self.scripts.rtime_from_range("20:00-22:00")
            self.scripts.rtime_from_range("02:51-2:51"), 
            self.scripts.rtime_from_range("02:24-02:25")
            ]
        print(*self.input_time)

    def phase_1(self, username: str, password: str, link: str) -> None:
        def like() -> None:
            try:
                like_button = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[3]/div[1]/div[1]/span[1]/div/div')
                like_button.click()
            except Exception as ex:
                print(f"Ошибка выставления лайка\nusername >>> {username}\nlink >>> {link}")
                # print(f"Like\n{ex}")
            self.scripts.have_a_rest(1)
        def comment() -> None:
            try:
                smile = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/section/div/form/div/div[1]/div/div')
                sleep(5)
                smile.click()
                sleep(5)
                smile.click()
                sleep(5)
                comment_area = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/section/div/form/div/textarea')
                sleep(5)
                comment_area.send_keys(self.words[randint(0, len(self.words) - 1)])
                sleep(5)
                confirm_button = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/section/div/form/div/div[2]/div')
                sleep(5)
                confirm_button.click()
                sleep(5)
            except Exception as ex:
                print(f"Ошибка выставления коммента\nusername >>> {username}\nlink >>> {link}")
                # print(f"comment\n{ex}")
            self.scripts.have_a_rest(1)
        def saves() -> None:
            try:
                save_button = browser.find_element(By.XPATH,'/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[3]/div[1]/div[3]/div/div/div/div')
                save_button.click()
            except Exception as ex:
                print(f"Ошибка сохранения\nusername >>> {username}\nlink >>> {link}")
                # print(f"Save\n{ex}")
            self.scripts.have_a_rest(1)
        # super().phase_1()
        # connect to browser
        try:
            options = selenium.webdriver.chrome.options.ChromiumOptions()
            options.add_argument("--start-maximized")
            browser = webdriver.Chrome(r"C:\Users\Наташа\PycharmProjects\MAINproject\driver\chromedriver.exe", options=options)
            # browser = webdriver.Chrome(options=options)
            browser.get('https://www.instagram.com')
        except Exception as ex:
            print(f"Driver error {ex}")
            return None

        self.scripts.have_a_rest(5)
        # send username and password
        try:
            username_input = browser.find_element(By.NAME, "username")
            username_input.clear()
            username_input.send_keys(username)
        except Exception as ex:
            print(f"Username input error\nusername >>> {username}\nlink >>> {link}")
            # print(f"Username input error {ex}")
        self.scripts.have_a_rest(1)
        try:
            password_input = browser.find_element(By.NAME, "password")
            password_input.clear()
            password_input.send_keys(password)
            self.scripts.have_a_rest(1)
            password_input.send_keys(Keys.ENTER)
        except Exception as ex:
            print(f"password input error\nusername >>> {username}\nlink >>> {link}")
            # print(f"Password input error \n {ex}")

        self.scripts.have_a_rest(4)

        browser.get(link)

        self.scripts.have_a_rest(4)

        # show history
        try:
            history_button = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/div/div/span')
            history_button.click()
            self.scripts.have_a_rest(5)

        except Exception as ex:
            print(f"Нет истории или ошибка истории\nusername >>> {username}\nlink >>> {link}")
            # print(f"History\n{ex}")
        finally:
            # find href
            browser.get(link)
            self.scripts.have_a_rest(3)
            try:
                hrefs = browser.find_elements(By.TAG_NAME, 'a')
                current_links = [item.get_attribute('href') for item in hrefs if '/p/' in item.get_attribute('href')]
                visited, max_visited = 0, randint(7, 12)
            except Exception as ex:
                print(f"Ошибка поиска постов\nusername >>> {username}\nlink >>> {link}")
            for l in current_links:
                if visited >= max_visited:
                    break
                else:
                    visited += 1
                browser.get(l)
                self.scripts.have_a_rest(2)

                # try click on sound button
                try:
                    sound_button = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[1]/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/button')
                    sound_button.click()
                    self.scripts.have_a_rest(1)
                except Exception as ex:
                    print(f"Не видео или ошибка видео\nusername >>> {username}\nlink >>> {link}")
                    # print(f"Sound\n{ex}")
                finally:
                    r_number = randint(1, 100)
                    if r_number in range(1, 41): 
                        ...
                    elif r_number in range(41, 76): 
                        like()
                    elif r_number in range(76, 91): 
                        like(), comment()
                    else: 
                        like(), comment(), saves()
        try:
            # try subscribe
            subscribe_button = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[1]/header/div[2]/div[1]/div[2]/button/div/div')
            subscribe_button.click()
            self.scripts.have_a_rest(3)
        except Exception as ex:
            print(f"Ошибка подписки\nusername >>> {username}\nlink >>> {link}")
            # print(f"Subscribe\n{ex}")
        browser.close()
        browser.quit()

    def phase_2(self, href, key):
        def expose(bots: str, href: str) -> None:
            def like() -> None:
                try:
                    like_button = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[3]/div[1]/div[1]/span[1]/div/div')
                    like_button.click()
                except Exception as ex:
                    print(f"Ошибка выставления лайка\nusername >>> {username}\nlink >>> {link}")
                    # print(f"Like\n{ex}")
                self.scripts.have_a_rest(1)
            def comment() -> None:
                try:
                    smile = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/section/div/form/div/div[1]/div/div')
                    sleep(5)
                    smile.click()
                    sleep(5)
                    smile.click()
                    sleep(5)
                    comment_area = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/section/div/form/div/textarea')
                    sleep(5)
                    comment_area.send_keys(self.words[randint(0, len(self.words) - 1)])
                    sleep(5)
                    confirm_button = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/section/div/form/div/div[2]/div')
                    sleep(5)
                    confirm_button.click()
                    sleep(5)
                except Exception as ex:
                    print(f"Ошибка выставления коммента\nusername >>> {username}\nlink >>> {link}")
                    # print(f"comment\n{ex}")
                self.scripts.have_a_rest(1)
            def saves() -> None:
                try:
                    save_button = browser.find_element(By.XPATH,'/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[3]/div[1]/div[3]/div/div/div/div')
                    save_button.click()
                except Exception as ex:
                    print(f"Ошибка сохранения\nusername >>> {username}\nlink >>> {link}")
                    # print(f"Save\n{ex}")
                self.scripts.have_a_rest(1)
            
            username = self.bots_data[bots]['username']
            password = self.bots_data[bots]['password']
            try:
                options = selenium.webdriver.chrome.options.ChromiumOptions()
                options.add_argument("--start-maximized")
                browser = webdriver.Chrome(r"C:\Users\Наташа\PycharmProjects\MAINproject\driver\chromedriver.exe", options=options)
                # browser = webdriver.Chrome(options=options)
                browser.get('https://www.instagram.com')
            except Exception as ex:
                print(f"Driver error {ex}")
                return None

            self.scripts.have_a_rest(5)
            try:
                username_input = browser.find_element(By.NAME, "username")
                username_input.clear()
                username_input.send_keys(username)
            except Exception as ex:
                print(f"Username input error (phase2)\nusername >>> {username}\nlink >>> {href}")
            self.scripts.have_a_rest(1)
            try:
                password_input = browser.find_element(By.NAME, "password")
                password_input.clear()
                password_input.send_keys(password)
                self.scripts.have_a_rest(1)
                password_input.send_keys(Keys.ENTER)
            except Exception as ex:
                print(f"password input error (phase2)\nusername >>> {username}\nlink >>> {href}")

            self.scripts.have_a_rest(4)

            browser.get(href)

            self.scripts.have_a_rest(4)

            r_number = randint(1, 100)
        
            if r_number in range(1, 76): 
                like()
            elif r_number in range(76, 91): 
                like(), comment()
            else: 
                like(), comment(), saves()
            


        signed_bots = self.users_data[key]['signed_bots']
        days = day1, day2, day3 = self.scripts.split_list(signed_bots)
        current_day = 0

        # Бахаем скрипты на сегодняшний день (Это current_day 0)
        #####################################################################################################################################
        timepoints = self.scripts.get_random_timepoints(start_time=datetime.datetime.now().strftime("%H:%M"), end_time='23:59', num_points=3)
        day1_1, day1_2, day1_3 = self.scripts.split_list(day1)
        while True:
            if datetime.datetime.now().strftime("%H:%M") == timepoints[0]:
                if day1_1 != []:
                    for bots in day1_1:
                        # run phase3 (bots, href=const)
                        expose(bots, href)
            elif datetime.datetime.now().strftime("%H:%M") == timepoints[1]:
                if day1_2 != []:
                    for bots in day1_2:
                        # run phase3 (bots, href=const)
                        expose(bots, href)
            elif datetime.datetime.now().strftime("%H:%M") == timepoints[2]:
                if day1_3 != []:
                    for bots in day1_3:
                        # run phase3 (bots, href=const)
                        expose(bots, href)
                break
        #####################################################################################################################################
        while True:
            if datetime.datetime.now().strftime("%H:%M") == "00:00":
                current_day += 1
                match current_day:
                    case 1:
                        # Действия под второй день
                        timepoints = self.scripts.get_random_timepoints(start_time=datetime.datetime.now().strftime("%H:%M"), end_time='23:59', num_points=3)
                        day2_1, day2_2, day2_3 = self.scripts.split_list(day1)
                        while True:
                            if datetime.datetime.now().strftime("%H:%M") == timepoints[0]:
                                if day2_1 != []:
                                    for bots in day2_1:
                                        # run phase3 (bots, href=const)
                                        expose(bots, href)
                            elif datetime.datetime.now().strftime("%H:%M") == timepoints[1]:
                                if day2_2 != []:
                                    for bots in day2_2:
                                        # run phase3 (bots, href=const)
                                        expose(bots, href)
                            elif datetime.datetime.now().strftime("%H:%M") == timepoints[2]:
                                if day2_3 != []:
                                    for bots in day2_3:
                                        # run phase3 (bots, href=const)
                                        expose(bots, href)
                                break
                    case 2:
                        # Действия под третий день
                        timepoints = self.scripts.get_random_timepoints(start_time=datetime.datetime.now().strftime("%H:%M"), end_time='23:59', num_points=3)
                        day3_1, day3_2, day3_3 = self.scripts.split_list(day1)
                        while True:
                            if datetime.datetime.now().strftime("%H:%M") == timepoints[0]:
                                if day3_1 != []:
                                    for bots in day3_1:
                                        expose(bots, href)
                            elif datetime.datetime.now().strftime("%H:%M") == timepoints[1]:
                                if day3_2 != []:
                                    for bots in day3_2:
                                        expose(bots, href)
                            elif datetime.datetime.now().strftime("%H:%M") == timepoints[2]:
                                if day3_3 != []:
                                    for bots in day3_3:
                                        expose(bots, href)
                                break
                    case 3:
                        # Завершение процесса (Выход)
                        return 0

    def start(self):
        # Если и ебанет то только тут
        # self.phase_1(username="+79280113665", password="Potriot13041974!", link="https://www.instagram.com/kimfelix143/")

        while True:
            if datetime.datetime.now().strftime("%H:%M") == "00:00":
                self.input_time = [
                self.scripts.rtime_from_range("07:00-9:00"), 
                self.scripts.rtime_from_range("20:00-22:00")
                ]

            queue = Queue()
            launch = Process(target=self.launch_detector, args=(queue, ), daemon=False)
            update = Process(target=self.update_detector, args=(queue, ), daemon=False)

            launch.start()
            launch.join()

            update_data = queue.get()
            if update_data is not None:
                self.users_data
                for key, value in self.users_data.items():
                    if key in list(update_data.keys()):
                        self.users_data[key]['signed_bots'].append(update_data[key])
                with open("d_data/users.json", 'w') as users_data:
                    json.dump(self.users_data, users_data, ensure_ascii=False, indent=4)

            update.start()
            update.join()

            update_data: dict = queue.get()
            if update_data is not None:
                for key, value in self.users_data.items():
                    if key in update_data.keys():
                        self.users_data[key]['href'] = update_data[key]
                with open("d_data/users.json", 'w') as users_data:
                    json.dump(self.users_data, users_data, ensure_ascii=False, indent=4)

    # Уважаемый примат читающий это завтра - не забудь try catch везде проставить. Процессы же ультанут - пезда бд будет

    def launch_detector(self, queue):
        current_time = datetime.datetime.now().strftime("%H:%M")
        if current_time == self.input_time[0] or current_time == self.input_time[1]:
            update_data = {}
            bots_name = list(self.bots_data.keys())
            defs = []
            for key, value in self.users_data.items():
                bot_name = self.scripts.get_random_unique_element(bots_name, value['signed_bots'])
                if bot_name is not None:
                    username = self.bots_data[bot_name]['username']
                    password = self.bots_data[bot_name]['password']
                    link = value['main_links']
                    process = Process(target=self.phase_1, args=(username, password, link), daemon=False)
                    update_data[key] = bot_name
                    defs.append(process)
            if len(defs) != 0:
                for process in defs:
                    self.scripts.have_a_rest(2)
                    process.start()
                for process in defs:
                    process.join()
            if update_data != {}:
                queue.put(update_data)
            else:
                queue.put(None)
        else:
            queue.put(None)

    def update_detector(self, queue: Queue):
        # Пробегаем по человечкам
        # Сверяем 
        # если что запускаем фазу 2
        try:
            options = selenium.webdriver.chrome.options.ChromiumOptions()
            options.add_argument("--start-maximized")
            browser = webdriver.Chrome(r"C:\Users\Наташа\PycharmProjects\MAINproject\driver\chromedriver.exe", options=options)
            browser.get('https://www.instagram.com')
        except Exception as ex:
            print(f"Driver error {ex}")
            return None
        
        self.scripts.have_a_rest(5)

        try:
            username_input = browser.find_element(By.NAME, "username")
            username_input.clear()
            username_input.send_keys(self.main_data['username'])
        except Exception as ex:
            print(f"Username input error\nusername >>> {self.main_data['username']}")
        self.scripts.have_a_rest(1)
        try:
            password_input = browser.find_element(By.NAME, "password")
            password_input.clear()
            password_input.send_keys(self.main_data['password'])
            self.scripts.have_a_rest(1)
            password_input.send_keys(Keys.ENTER)
        except Exception as ex:
            print(f"password input error\nusername >>> {self.main_data['username']}")

        self.scripts.have_a_rest(4)

        answer = {

        }

        for key, value in self.users_data.items():
            browser.get(self.users_data[key]['main_links'])
            self.scripts.have_a_rest(4)

            try:
                hrefs = browser.find_elements(By.TAG_NAME, 'a')
                current_links = [item.get_attribute('href') for item in hrefs if '/p/' in item.get_attribute('href')]
            except Exception as ex:
                print(f"Ошибка поиска поста в update")

            if "href" in self.users_data[key].keys():
                if self.users_data[key]['href'] != current_links[0]:
                    answer[key] = current_links[0]
                    # run phase 2
                    phase_two = Process(target=self.phase_2, args=(current_links[0], key), daemon=False)
                    phase_two.start()
            else:
                answer[key] = current_links[0]
            self.scripts.have_a_rest(2)
        if answer != {}:
            queue.put(answer)
        else:
            queue.put(None)


class Scripts:
    def __init__(self):
        ...

    @staticmethod
    def split_list(list1):
        total_elements = len(list1)

        # Вычисляем количество элементов для каждого списка на основе пропорций
        size_list2 = total_elements // 2
        size_list3 = total_elements * 3 // 10
        size_list4 = total_elements * 2 // 10

        # Разделяем список на три части
        list2 = list1[:size_list2]
        list3 = list1[size_list2:size_list2 + size_list3]
        list4 = list1[size_list2 + size_list3:]

        return list2, list3, list4

    @staticmethod
    def get_random_unique_element(list1, list2):
        """Возвращает случайный элемент из списка 1, который отсутствует в списке 2."""
        unique_elements = list(set(list1) - set(list2))
        if unique_elements:
            return choice(unique_elements)
        else:
            return None
        
    @staticmethod
    def rtime_from_range(rang: str = "00:00-23:00") -> list | None:
        def convert_to_sec(value: str) -> int:
            value = list(map(int, value.split(":")))
            value = value[0] * 60 + value[1]
            return value
        def convert_to_time(value: int) -> str:
            div = value // 60
            mod = value % 60
            return f"{div if len(str(div)) == 2 else '0' + str(div)}:{mod if len(str(mod)) == 2 else '0' + str(mod)}"
        rang = list(map(convert_to_sec, rang.split("-")))
        return convert_to_time(randint(rang[0], rang[1]))

    @staticmethod
    def have_a_rest(mode: int) -> None:
        """
            mode:
            1 -> (1;5)
            2 -> (5;10)
            3 -> (10;20)
            4 -> (20;30)
            5 -> (30;40)
            :param mode:
            :return: None
        """
        match mode:
            case 1:
                sleep(randint(2, 5))
            case 2:
                sleep(randint(5, 10))
            case 3:
                sleep(randint(10, 20))
            case 4:
                sleep(randint(20, 30))
            case 5:
                sleep(randint(30, 40))
            case _:
                print("Invalid mode")

    @staticmethod
    def get_random_timepoints(start_time, end_time, num_points):
        start_dt = datetime.datetime.strptime(start_time, '%H:%M')
        end_dt = datetime.datetime.strptime(end_time, '%H:%M')

        # Вычисляем разницу между временем включения программы и "23:59"
        total_time = end_dt - start_dt

        # Вычисляем интервал между временными точками
        interval = total_time / (num_points + 1)

        # Список для хранения временных точек
        timepoints = []

        # Вычисляем временные точки
        current_time = start_dt + interval
        for _ in range(num_points):
            timepoints.append(current_time.strftime('%H:%M'))
            current_time += interval

        return timepoints
    
    @staticmethod
    def increase_time_randomly(time_str):
        # Преобразуем строку времени в объект datetime
        time_obj = datetime.datetime.strptime(time_str, '%H:%M')

        # Вычисляем случайное количество времени в пределах 1.5 часа
        random_time_delta = datetime.timedelta(hours=uniform(0, 1.5))

        # Увеличиваем время на случайный интервал
        increased_time = time_obj + random_time_delta

        # Форматируем результат в строку времени "%H:%M"
        increased_time_str = increased_time.strftime('%H:%M')

        return increased_time_str



if __name__ == '__main__':
    manager = Manager()
    manager.run()
