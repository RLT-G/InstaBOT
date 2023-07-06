__author__ = 'Konstantin Bychkov <inco.k.b.blizz@gmail.com>'
__copyright__ = 'Copyright 2023, RLT IP.'
__version__ = '0.1.7'


import json
import selenium.webdriver.chrome.options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from random import randint
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

    def phase_1(self, username: str, password: str, link: str) -> None:
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
            visited, max_visited = 0, randint(12, 20)
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
                    # try click on the like
                    if True:#randint(1, 10) in range(1, 5):
                        try:
                            like_button = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[3]/div[1]/div[1]/span[1]/div/div')
                            like_button.click()
                        except Exception as ex:
                            print(f"Like\n{ex}")
                        self.scripts.have_a_rest(1)
                        # try send comment
                        if True:#randint(1, 10) in range(1, 3):
                            try:

                                smile = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/section/div/form/div/div[1]/div/div')
                                # self.scripts.have_a_rest(1)
                                sleep(5)
                                smile.click()
                                # self.scripts.have_a_rest(2)
                                sleep(5)
                                smile.click()
                                # self.scripts.have_a_rest(1)
                                sleep(5)
                                comment_area = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/section/div/form/div/textarea')
                                # self.scripts.have_a_rest(1)
                                sleep(5)
                                comment_area.send_keys(self.words[randint(0, len(self.words) - 1)])
                                # self.scripts.have_a_rest(2)
                                sleep(5)
                                confirm_button = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/section/div/form/div/div[2]/div')
                                # self.scripts.have_a_rest(1)
                                sleep(5)
                                confirm_button.click()
                                sleep(5)
                                # self.scripts.have_a_rest(2)

                            except Exception as ex:
                                print(f"comment\n{ex}")
                            self.scripts.have_a_rest(2)
                            
                            # try click on save button
                            if True:#randint(1, 10) == 1:
                                try:
                                    save_button = browser.find_element(By.XPATH,'/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[3]/div[1]/div[3]/div/div/div/div')
                                    save_button.click()
                                except Exception as ex:
                                    print(f"Save\n{ex}")
                    self.scripts.have_a_rest(2)
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
        ...

    def start(self):
        self.phase_1(username="+79280113665", password="Potriot13041974!", link="https://www.instagram.com/crescentt/")
        
    def exit(self):
        ...


class Scripts:
    def __init__(self):
        ...

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
                sleep(randint(1, 5))
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
