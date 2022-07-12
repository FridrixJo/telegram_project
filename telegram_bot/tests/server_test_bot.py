import time

from aiogram import Bot, types
from aiogram import Dispatcher
from aiogram.utils import executor
import asyncio

bot = Bot(token='5583638970:AAE4WgvD77v0eMv1wBEdVkSPCFlSxQUse9U')
dispatcher = Dispatcher(bot=bot)


@dispatcher.message_handler(commands=['menu'])
async def start(message: types.Message):
    await bot.send_message(message.chat.id, 'hola')
    await bot.send_message(message.chat.id, 'i am bot')

try:
    asyncio.run(executor.start_polling(dispatcher=dispatcher, skip_updates=False))
except Exception as error:
    print(error)

