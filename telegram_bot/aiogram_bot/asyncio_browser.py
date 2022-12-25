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
            # self.browser = await launch(options={"headless": False})
            self.page = await self.browser.newPage()
            await self.page.setUserAgent('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36')
            await self.page.setExtraHTTPHeaders({
                "X-Frame-Options": "GOFORIT"
            })
            print(type(self.browser), type(self.page))
        except Exception as e:
            await self.close()
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
                await self.close()
                print(e)

        except Exception as e:
            await self.close()
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
            await self.close()
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
            await self.close()
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
                    return False, 'alarm'
            except Exception as e:
                await self.close()
                print(e)

        except Exception as e:
            await self.close()
            return False, e

        errors_db.set_error_status(self.phone, 'passed password')

        return True, 'OK'

    async def get_api(self, errors_db: ErrorsDB):
        try:
            errors_db.set_error_status(self.phone, 'gonna follow link')

            await self.page.goto('https://my.telegram.org/apps')

            await asyncio.sleep(1)

            errors_db.set_error_status(self.phone, 'gonna get all groups')

            groups = await self.page.querySelectorAll('div.form-group')
            print(len(groups), 'aye')

            if len(groups):
                try:
                    app_title = ''.join(random.choice(string.ascii_letters) for _ in range(random.randrange(8, 10)))
                    short_name = ''.join(random.choice(string.ascii_letters) for _ in range(random.randrange(8, 10)))
                    print(app_title, short_name)

                    app_title_input = await self.page.querySelector('input#app_title.form-control.input-xlarge')
                    short_name_input = await self.page.querySelector('input#app_shortname.form-control.input-xlarge')

                    await asyncio.sleep(1)

                    errors_db.set_error_status(self.phone, 'gonna insert app_title')
                    await app_title_input.type(app_title)

                    await asyncio.sleep(1)

                    errors_db.set_error_status(self.phone, 'gonna insert short_name')
                    await short_name_input.type(short_name)

                    errors_db.set_error_status(self.phone, 'gonna get btn')

                    btn = await self.page.querySelector('button#app_save_btn')

                    await asyncio.sleep(1)

                    await btn.press('Enter')

                    errors_db.set_error_status(self.phone, 'pressed btn')

                except Exception as e:
                    await self.close()
                    print(e, 'create_application')
                    return 0, 0, self.phone, False, 'sww'

            errors_db.set_error_status(self.phone, 'gonna get all groups')

            all_groups = await self.page.querySelectorAll('div.form-group')
            if len(all_groups) == 12:
                input_groups = await self.page.querySelectorAll('span.uneditable-input')

                if len(input_groups):
                    print(len(input_groups))
                    errors_db.set_error_status(self.phone, 'ready to get api_id')
                    api_id = await self.page.evaluate('(element) => element.textContent', input_groups[0])

                    errors_db.set_error_status(self.phone, 'ready to get api_hash')
                    api_hash = await self.page.evaluate('(element) => element.textContent', input_groups[1])
                else:
                    await self.close()
                    return 0, 0, self.phone, False, 'there are not needed fields'
            else:
                await self.close()
                return 0, 0, self.phone, False, 'there are not needed fields'

        except Exception as e:
            print(e, 'get_api')
            await self.close()
            return 0, 0, self.phone, False, e

        errors_db.set_error_status(self.phone, 'got data + ready to close browser')

        await self.close()

        errors_db.set_error_status(self.phone, 'success')

        print('all is well')

        return api_id, api_hash, self.phone, True, 'OK'







