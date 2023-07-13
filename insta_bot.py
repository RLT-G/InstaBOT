__author__ = 'Konstantin Bychkov <inco.k.b.blizz@gmail.com>'
__copyright__ = 'Copyright 2023, RLT IP.'
__version__ = '0.2.8'


from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import selenium.webdriver.chrome.options
from selenium import webdriver

from multiprocessing import Process, Queue
from random import randint, choice
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

    def start(self):
        ...

    def exit(self):
        ...

    def phase_1(self, username: str, password: str, link: str):
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
        if len(sys.argv) > 1:
            if sys.argv[1] is not None:
                self.executor(sys.argv[1])
        else:
            while True: self.executor(input(" >>> "))


class Manager(ManagerBase):
    def __init__(self):
        super().__init__()
        self.scripts = Scripts()
        self.words = self.use_json("d_data/comments.json")["comments"]
        self.users_data = self.use_json("d_data/users.json")
        self.bots_data = self.use_json("d_data/bots.json")
        self.input_time = [
            self.scripts.rtime_from_range("07:00-9:00"), 
            self.scripts.rtime_from_range("20:00-22:00")
            ]

    def phase_1(self, username: str, password: str, link: str) -> None:
        def like() -> None:
            try:
                like_button = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[3]/div[1]/div[1]/span[1]/div/div')
                like_button.click()
            except Exception as ex:
                print(f"Like\n{ex}")
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
                print(f"comment\n{ex}")
            self.scripts.have_a_rest(1)
        def saves() -> None:
            try:
                save_button = browser.find_element(By.XPATH,'/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[3]/div[1]/div[3]/div/div/div/div')
                save_button.click()
            except Exception as ex:
                print(f"Save\n{ex}")
            self.scripts.have_a_rest(1)
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
            print(f"Username input error {ex}")
        self.scripts.have_a_rest(1)
        try:
            password_input = browser.find_element(By.NAME, "password")
            password_input.clear()
            password_input.send_keys(password)
            self.scripts.have_a_rest(1)
            password_input.send_keys(Keys.ENTER)
        except Exception as ex:
            print(f"Password input error \n {ex}")

        self.scripts.have_a_rest(4)

        browser.get(link)

        self.scripts.have_a_rest(4)

        # show history
        try:
            history_button = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/div/div/span')
            history_button.click()
            self.scripts.have_a_rest(5)

        except Exception as ex:
            print(f"History\n{ex}")
        finally:
            # find href
            browser.get(link)
            self.scripts.have_a_rest(3)
            hrefs = browser.find_elements(By.TAG_NAME, 'a')
            current_links = [item.get_attribute('href') for item in hrefs if '/p/' in item.get_attribute('href')]
            visited, max_visited = 0, randint(7, 12)
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
                    print(f"Sound\n{ex}")
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
            print(f"Subscribe\n{ex}")
        browser.close()
        browser.quit()

    def phase_2(self):
        # в первый день 50% ботов работают В 2й 30% в 3й 20%
        # В течение дня по 4 временным рамкам порвну запускаем ботов на лайки

        # Пишем метод на тупо лайк с коментом и прочей хуйней
        # выплываем из говна и радуемся
        ...

    def start(self):
        # Если и ебанет то только тут
        # self.phase_1(username="+79280113665", password="Potriot13041974!", link="https://www.instagram.com/kimfelix143/")
        while True:
            queue = Queue()
            if datetime.datetime.now().strftime("%H:%M") == "00:00":
                self.input_time = [
                self.scripts.rtime_from_range("07:00-9:00"), 
                self.scripts.rtime_from_range("20:00-22:00")
                ]

            launch = Process(target=self.launch_detector, args=(queue, ), daemon=False)
            update = Process(target=self.update_detector, daemon=False)

            launch.start()
            update.start()

            launch.join()
            update_data = queue.get()
            if update_data is not None:
                self.users_data
                for key, value in self.users_data.items():
                    if key in list(update_data.keys()):
                        self.users_data[key]['signed_bots'].append(update_data[key])
                with open("d_data/users.json", 'w') as users_data:
                    json.dump(self.users_data, users_data)

            update.join()

    # Уважаемый примат читающий это завтра - не забудь try catch везде проставить. Процессы же ультанут - пезда бд будет

    def launch_detector(self, queue):
        # Ну или тут
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
                    process.start()
                for process in defs:
                    process.join()
            if update_data != {}:
                queue.put(update_data)
            else:
                queue.put(None)
        else:
            queue.put(None)

    def update_detector(self):
        # Пробегаем по человечкам
        # Сверяем 
        # если что запускаем фазу 2
        ...
        
    def exit(self):
        ...


class Scripts:
    def __init__(self):
        ...

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
            :return:
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


if __name__ == '__main__':
    manager = Manager()
    manager.run()
