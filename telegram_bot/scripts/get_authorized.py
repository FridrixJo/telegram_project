#!/usr/bin/python
# -*- coding: utf8 -*-
import string

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time
import random

class Api_Data:
    def __init__(self):
        self.main_link = "https://my.telegram.org/auth"
        self.apps_link = "https://my.telegram.org/apps"

    def login(self, phone_number):
        browser = webdriver.Chrome('../driver/chromedriver.exe')
        try:
            browser.get(self.main_link)
        except Exception as e:
            print(e, "main_link error")
            return

        time.sleep(random.randrange(3,5))

        try:
            form1 = browser.find_element(By.CSS_SELECTOR, 'form#my_send_form')
            login_phone = form1.find_element(By.CLASS_NAME, 'input-large')
            login_phone.clear()
            login_phone.send_keys(str(phone_number))
            #79954581302 std::cout<<cpp
            #79639243583 the blond done
            #79161854870 artem
            #79657279473 валентин
            #79919496926 макс
            #79670170740 moliden
            #79119178067 olivero

        except Exception as e:
            print(e, "login_input error")
            return

        time.sleep(random.randrange(2,4))

        #password = browser.find_element(By.ID, 'my_password')
        #password.send_keys('password')"""

        try:
            button1 = form1.find_element(By.CLASS_NAME, 'btn-lg')
            button1.send_keys(Keys.ENTER)
        except Exception as e:
            print(e, "submit button #1")
            return

        time.sleep(random.randrange(7,15))

        try:
            form2 = browser.find_element(By.CSS_SELECTOR, 'form#my_login_form')
            button2 = form2.find_element(By.CLASS_NAME, 'btn-lg')
            button2.send_keys(Keys.ENTER)
        except Exception as e:
            print(e, "submit button #2")

        time.sleep(random.randrange(2,3))

        browser.get(self.apps_link)
        time.sleep(random.randrange(1,2))

        create_btn = browser.find_elements(By.ID, 'app_save_btn')

        if create_btn[0].text == 'Create application':
            try:
                app_title = ''.join(random.choice(string.digits + string.ascii_letters) for _ in range(random.randrange(8, 25)))
                short_name = ''.join(random.choice(string.digits + string.ascii_letters) for _ in range(random.randrange(8, 25)))

                app_title_input = browser.find_element(By.ID, 'app_title')
                app_shortname_input = browser.find_element(By.ID, 'app_shortname')

                app_title_input.send_keys(app_title)
                time.sleep(random.randrange(2,5))

                app_shortname_input.send_keys(short_name)
                time.sleep(random.randrange(1,3))

                create_btn[0].send_keys(Keys.ENTER)

                time.sleep(1)
            except Exception as e:
                print(e, "creating application")
                return

        browser.refresh()
        browser.get_screenshot_as_file('screen.png')

        try:
            forms = browser.find_elements(By.CLASS_NAME, 'form-group')
            #print(len(forms))

            api_id = forms[0].find_element(By.TAG_NAME, 'strong').text
            api_hash = forms[1].find_element(By.CSS_SELECTOR, 'span.uneditable-input').text

            browser.close()
            browser.quit()

            print(api_id, api_hash, phone_number)
            return api_id, api_hash, phone_number
        except Exception as e:
            print(e, "getting api_id, api_hash")
            return


