from aiogram import Bot, types
from aiogram.types import ContentType
from aiogram import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

storage = MemoryStorage()

bot = Bot(token='5583638970:AAE9RTGf3u3hzbvV9VkhwJfQSRXfQfuwRxw')
dispatcher = Dispatcher(bot=bot, storage=storage)


@dispatcher.message_handler(content_types=[ContentType.PHOTO])
async def start(message: types.Message):
    print(1)
    with open('file.png', 'wb') as file:
        file.write(message.photo)

    #await bot.send_photo(message.chat.id, message.photo)

try:
    asyncio.run(executor.start_polling(dispatcher=dispatcher, skip_updates=False))
except Exception as e:
    print(e)
