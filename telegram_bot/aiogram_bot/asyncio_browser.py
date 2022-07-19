import asyncio

from pyppeteer import browser
from pyppeteer import page
from pyppeteer import launch
import random
import string


class WebScraper:
    def __init__(self):
        self.browser: browser.Browser
        self.page: page.Page
        self.phone: str

    async def initialize(self):
        try:
            self.browser = await launch(options={"args": ['--no-sandbox']})
            self.page = await self.browser.newPage()
            print(type(self.browser), type(self.page))
        except Exception as e:
            print(e)
            return False, 'sww'

        print('OK')
        return True, 'OK'

    async def close(self):
        try:
            await self.browser.close()
        except Exception as e:
            print(e)

    async def input_phone_number(self, phone_number: str):
        try:
            self.phone = phone_number

            await self.page.goto('https://my.telegram.org/auth')

            await asyncio.sleep(1)

            btn = await self.page.querySelector('div.support_submit > button.btn-lg')

            await self.page.type('div.form-group > input.input-large', phone_number)

            await asyncio.sleep(1)

            await btn.press('Enter')

            await asyncio.sleep(1)

            errors = await self.page.querySelectorAll('div.alert-danger')
            if len(errors):
                return False, 'alarm'
        except Exception as e:
            print(e)
            return False, e

        return True, 'OK'

    async def remove_number_error(self):
        await asyncio.sleep(1)
        try:
            error = await self.page.querySelector('div.alert-danger > a.close')
            await error.press('Enter')
            await asyncio.sleep(1)
            input_number = await self.page.querySelector('div.form-group > input.input-large')
            number = await self.page.evaluate('(element) => element.value', input_number)
            print(number)
            for _ in range(len(number)):
                await input_number.press('Backspace')

        except Exception as e:
            print(e)
            return False, e

        return True, 'OK'

    async def remove_password_error(self):
        await asyncio.sleep(1)
        try:
            error = await self.page.querySelector('div.alert-danger > a.close')
            await error.press('Enter')
            await asyncio.sleep(1)
            input_password = await self.page.querySelector('div.form-group > input#my_password')
            password = await self.page.evaluate('(element) => element.value', input_password)
            print(password)
            for _ in range(len(password)):
                await input_password.press('Backspace')

        except Exception as e:
            print(e)
            return False, e

        return True, 'OK'

    async def input_password(self, password: str):
        try:
            await asyncio.sleep(1)

            btn = await self.page.querySelector('div.support_submit > button.btn-lg')

            await self.page.type('div.form-group > input#my_password', password)

            await asyncio.sleep(1)

            await btn.press('Enter')

            await asyncio.sleep(1)

            errors = await self.page.querySelectorAll('div.alert-danger')
            if len(errors):
                print('alarm')
                return False, 'alarm'

        except Exception as e:
            return False, e

        return True, 'OK'

    async def get_api(self):
        try:
            await asyncio.sleep(1)

            await self.page.goto('https://my.telegram.org/apps')

            await asyncio.sleep(1)

            check_group = await self.page.querySelectorAll('span.uneditable-input')

            if len(check_group) == 0:
                app_title = ''.join(random.choice(string.digits + string.ascii_letters) for _ in range(random.randrange(8, 25)))
                short_name = ''.join(random.choice(string.digits + string.ascii_letters) for _ in range(random.randrange(8, 25)))
                print(app_title, short_name)

                await self.page.type('input#app_title', app_title)
                await self.page.type('input#app_shortname', short_name)

                await asyncio.sleep(1)

                btn = await self.page.querySelector('button.btn-primary')
                await btn.press('Enter')

                await asyncio.sleep(1)

            check_group = await self.page.querySelectorAll('span.uneditable-input')
            api_id = await self.page.evaluate('(element) => element.textContent', check_group[0])
            api_hash = await self.page.evaluate('(element) => element.textContent', check_group[1])
        except Exception as e:
            print(e)
            await self.browser.close()
            return 0, 0, self.phone, False, e

        await self.browser.close()
        return api_id, api_hash, self.phone, True, 'OK'






