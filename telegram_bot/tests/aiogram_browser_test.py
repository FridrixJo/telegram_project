

import asyncio
from pyppeteer import launch
import random


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

        #input_number_field = await self.page.querySelector('div.form-group > input.input-large')
        btn = await self.page.querySelector('div.support_submit > button.btn-lg')

        await self.page.type('div.form-group > input.input-large', phone_number)

        await asyncio.sleep(2)

        await btn.press('Enter')

    async def input_password(self, password: str):

        await asyncio.sleep(1)

        #input_password_field = await self.page.querySelector('div.form-group > input#my_password')
        btn = await self.page.querySelector('div.support_submit > button.btn-lg')

        await self.page.type('div.form-group > input#my_password', password)

        await asyncio.sleep(1)

        await btn.press('Enter')

    async def get_api(self):
        await asyncio.sleep(2)

        await self.page.goto('https://my.telegram.org/apps')

        await asyncio.sleep(1)

        btn = await self.page.querySelector('button.btn-primary')
        print(btn.getProperties())


async def main():
    scraper = WebScraper()
    await scraper.initialize()

    phone = input('phone? ... ')
    await scraper.input_password(phone)

    password = input('password? ...')
    await scraper.input_password(password)

    await scraper.get_api()

asyncio.get_event_loop().run_until_complete(main())


