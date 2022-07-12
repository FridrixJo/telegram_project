#!/usr/bin/python
# -*- coding: utf8 -*-
import string

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions

opts = ChromeOptions()
opts.add_argument("--headless")

import asyncio

import random


class Api_Data:
    def __init__(self, phone_number):
        self.main_link = "https://my.telegram.org/auth"
        self.apps_link = "https://my.telegram.org/apps"
        self.phone_number = phone_number
        #self.browser = webdriver.Chrome("message_spreader/scripts/driver/chromedriver.exe")
        self.browser = webdriver.Chrome(options=opts, executable_path='../aiogram_bot/driver/chromedriver.exe')

    def browser_state(self):
        return self.phone_number

    async def login(self):
        try:
            self.browser.get(self.main_link)
        except Exception as e:
            print(e, "open_browser error")
            return False, 'open_browser error'

        await asyncio.sleep(random.randrange(1,2))

        try:
            form1 = self.browser.find_element(By.CSS_SELECTOR, 'form#my_send_form')
            login_phone = form1.find_element(By.CLASS_NAME, 'input-large')
            login_phone.clear()
            login_phone.send_keys(str(self.phone_number))
        except Exception as e:
            print(e, 'login_input error')
            return False, 'login_input error'

        await asyncio.sleep(random.randrange(1,2))

        try:
            form1 = self.browser.find_element(By.CSS_SELECTOR, 'form#my_send_form')
            button1 = form1.find_element(By.CLASS_NAME, 'btn-lg')
            button1.send_keys(Keys.ENTER)
        except Exception as e:
            print(e, "submit_button_1 error")
            return False, 'submit_button_1 error'

        try:
            await asyncio.sleep(1)
            errors = self.browser.find_elements(By.CLASS_NAME, 'alert-danger')
            if len(errors):
                return False, 'invalid number'
        except Exception as e:
            print(e)

        return True, 'OK'

    async def input_password(self, telegram_password):
        try:
            password = self.browser.find_element(By.ID, 'my_password')
            password.clear()
            password.send_keys(telegram_password)
        except Exception as e:
            print(e, 'inserting_password error')
            return False, 'inserting_password error'

        try:
            form1 = self.browser.find_element(By.CSS_SELECTOR, 'form#my_login_form')
            button1 = form1.find_element(By.CLASS_NAME, 'btn-lg')
            button1.send_keys(Keys.ENTER)
        except Exception as e:
            print(e, "submit button_2")
            return False, 'submit button_2'

        try:
            await asyncio.sleep(1)
            errors = self.browser.find_elements(By.CLASS_NAME, 'alert-danger')
            if len(errors):
                return False, 'invalid password'
        except Exception as e:
            print(e)

        return True, 'OK'

    async def remove_error(self):
        await asyncio.sleep(1)
        try:
            error = self.browser.find_element(By.CLASS_NAME, 'alert-danger')
            cross = error.find_element(By.CLASS_NAME, 'close')
            cross.send_keys(Keys.ENTER)
        except Exception as e:
            print(e, 'finding errors')
            return False, 'finding errors'

        await asyncio.sleep(1)

        return True, 'OK'

    async def getting_data(self):

        try:
            self.browser.refresh()
            self.browser.get(self.apps_link)

            create_btn = self.browser.find_elements(By.ID, 'app_save_btn')
        except Exception as e:
            print(e, 'getting apps_link error')
            return 0, 0, self.phone_number, False, 'getting apps_link error'

        if create_btn[0].text == 'Create application':
            try:
                app_title = ''.join(random.choice(string.digits + string.ascii_letters) for _ in range(random.randrange(8, 25)))
                short_name = ''.join(random.choice(string.digits + string.ascii_letters) for _ in range(random.randrange(8, 25)))

                app_title_input = self.browser.find_element(By.ID, 'app_title')
                app_shortname_input = self.browser.find_element(By.ID, 'app_shortname')

                app_title_input.send_keys(app_title)
                await asyncio.sleep(random.randrange(1,2))

                app_shortname_input.send_keys(short_name)
                await asyncio.sleep(random.randrange(1,2))

                create_btn[0].send_keys(Keys.ENTER)

                await asyncio.sleep(1)
            except Exception as e:
                print(e, "creating application error")
                return 0, 0, self.phone_number, False, 'creating application error'

        try:
            self.browser.refresh()
            forms = self.browser.find_elements(By.CLASS_NAME, 'form-group')

            api_id = forms[0].find_element(By.TAG_NAME, 'strong').text
            api_hash = forms[1].find_element(By.CSS_SELECTOR, 'span.uneditable-input').text

            self.browser.close()
            self.browser.quit()

            return api_id, api_hash, self.phone_number, True, 'OK'
        except Exception as e:
            print(e, "getting api_id, api_hash error")
            return 0, 0, self.phone_number, False, 'getting api_id, api_hash error'


