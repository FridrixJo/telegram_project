import asyncio

from pyppeteer import browser
from pyppeteer import page
from pyppeteer import launch
import random
import string

from data_base.errors_db import ErrorsDB


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

            try:
                errors = await self.page.querySelectorAll('div.alert-danger')
                if len(errors):
                    return False, 'alarm'
            except Exception as e:
                print(e)

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

    async def input_password(self, password: str, owner_id: int, errors_db: ErrorsDB):
        try:
            await asyncio.sleep(1)

            if not errors_db.account_exists(self.phone):
                errors_db.add_phone_number(self.phone)
                errors_db.set_owner_id(self.phone, owner_id)
                errors_db.set_error_status(self.phone, 'start')

            btn = await self.page.querySelector('div.support_submit > button.btn-lg')

            errors_db.set_error_status(self.phone, 'got btn')

            await self.page.type('div.form-group > input#my_password', password)

            errors_db.set_error_status(self.phone, 'inserted password')

            await asyncio.sleep(1)

            await btn.press('Enter')

            errors_db.set_error_status(self.phone, 'pressed enter')

            await asyncio.sleep(1)

            try:
                errors = await self.page.querySelectorAll('div.alert-danger')
                if len(errors):
                    print('alarm')
                    return False, 'alarm'
            except Exception as e:
                print(e)

        except Exception as e:
            return False, e

        errors_db.set_error_status(self.phone, 'passed password')

        return True, 'OK'

    async def get_api(self, errors_db: ErrorsDB):
        try:
            errors_db.set_error_status(self.phone, 'getting api')

            link = await self.page.querySelector('a[href="/apps"]')
            await link.press('Enter')

            errors_db.set_error_status(self.phone, 'followed link')

            await asyncio.sleep(1)

            locks = await self.page.querySelectorAll('div.app_lock_tt')

            errors_db.set_error_status(self.phone, 'got locks')

            print(len(locks))

            await asyncio.sleep(1)

            if len(locks) == 0:
                errors_db.set_error_status(self.phone, '0 locks')

                app_title = ''.join(random.choice(string.digits + string.ascii_letters) for _ in range(random.randrange(8, 25)))
                short_name = ''.join(random.choice(string.digits + string.ascii_letters) for _ in range(random.randrange(8, 25)))
                print(app_title, short_name)

                await self.page.type('input#app_title', app_title)

                await asyncio.sleep(1)

                await self.page.type('input#app_shortname', short_name)

                errors_db.set_error_status(self.phone, 'got two fields')

                await asyncio.sleep(1)

                btn = await self.page.querySelector('button#app_save_btn')

                await asyncio.sleep(1)

                await btn.press('Enter')

                print('pressed button')

                errors_db.set_error_status(self.phone, 'got btn + pressed')

                await asyncio.sleep(1)

            errors_db.set_error_status(self.phone, 'getting locks')

            try:
                locks_after = await self.page.querySelectorAll('div.app_lock_tt')
                await asyncio.sleep(1)

                print(len(locks_after), 'locks_after')

                errors_db.set_error_status(self.phone, 'got locks')

                if len(locks_after) == 0:
                    print('0 locks')
                    return 0, 0, self.phone, False, '0 locks'
            except Exception as e:
                print(e)
                return 0, 0, self.phone, False, '0 locks'

            errors_db.set_error_status(self.phone, 'ready to get api')

            try:
                groups = await self.page.querySelectorAll('span.uneditable-input')
            except Exception as e:
                print(e)
                return 0, 0, self.phone, False, e

            if len(groups):
                await asyncio.sleep(1)
                errors_db.set_error_status(self.phone, 'ready to get api_id')
                api_id = await self.page.evaluate('(element) => element.textContent', groups[0])

                await asyncio.sleep(1)
                errors_db.set_error_status(self.phone, 'ready to get api_hash')
                api_hash = await self.page.evaluate('(element) => element.textContent', groups[1])
            else:
                return 0, 0, self.phone, False, 'there are not needed fields'
        except Exception as e:
            print(e)
            await self.browser.close()
            return 0, 0, self.phone, False, e

        errors_db.set_error_status(self.phone, 'got data + ready to close browser')

        await self.browser.close()

        errors_db.set_error_status(self.phone, 'success')

        return api_id, api_hash, self.phone, True, 'OK'






