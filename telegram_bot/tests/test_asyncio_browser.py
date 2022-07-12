from aiogram_bot.asyncio_browser import WebScraper
import asyncio


async def start(app: WebScraper):
    phone = input('phone? ...')
    params = await app.input_phone_number(phone)
    if params[0]:
        password = input('password? ...')
        params = await app.input_password(password)

        if params[0]:
            await app.get_api()
        else:
            await app.remove_password_error()
            password = input('password? ...')
            params = await app.input_password(password)
            await app.get_api()
    else:
        await app.remove_number_error()
        phone = input('phone? ...')
        params = await app.input_phone_number(phone)


app = WebScraper()

try:
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start(app))

except Exception as e:
    print(e)

