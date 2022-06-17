import asyncio
from pyppeteer import launch
import random
import string


class WebScraper:
    def __init__(self):
        self.browser: None
        self.page: None

    async def initialize(self):
        self.browser = await launch({"headless": False, "args": ["--start-maximized"]})
        self.page = await self.browser.newPage()

    async def input_phone_number(self, phone_number: str):
        await self.page.goto('https://my.telegram.org/auth')

        await asyncio.sleep(1)

        input_number_field = await self.page.querySelector('div.form-group > input.input-large')
        btn = await self.page.querySelector('div.support_submit > button.btn-lg')

        await self.page.type('div.form-group > input.input-large', phone_number)

        await asyncio.sleep(2)

        await btn.press('Enter')

    async def input_password(self, password: str):

        await asyncio.sleep(1)

        input_password_field = await self.page.querySelector('div.form-group > input#my_password')
        btn = await self.page.querySelector('div.support_submit > button.btn-lg')

        await self.page.type('div.form-group > input#my_password', password)

        await asyncio.sleep(1)

        await btn.press('Enter')

    async def get_api(self):
        await asyncio.sleep(2)

        await self.page.goto('https://my.telegram.org/apps')

        await asyncio.sleep(1)

        btn = await self.page.querySelector('button.btn-primary')
        check_group = await self.page.querySelectorAll('div.form-group > span.uneditable-input')

        if len(check_group) == 0:
            app_title = ''.join(random.choice(string.digits + string.ascii_letters) for _ in range(random.randrange(8, 25)))
            short_name = ''.join(random.choice(string.digits + string.ascii_letters) for _ in range(random.randrange(8, 25)))

            await self.page.type('div.form-group > input#app_title', app_title)
            await asyncio.sleep(1)

            await self.page.type('div.form-group > input#app_shortname', short_name)
            await asyncio.sleep(1)

            await btn.press('Enter')
            await asyncio.sleep(2)





