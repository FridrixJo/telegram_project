import asyncio
import time

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType

from aiogram import types
import random
import string
from config import *
from key_boards import *
from FSMClasses import *
from urllib import request


from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from data_base.queue import QueueDB


storage = MemoryStorage()

bot = Bot(TOKEN)

dispatcher = Dispatcher(bot=bot, storage=storage)

ADMIN_IDS = [int(ADMIN_ID), 5405732922]

db = QueueDB('data_base/queue.db')

BACK_BTN = types.InlineKeyboardButton('Назад ↩️', callback_data='back')


async def clear_state(state: FSMContext):
    try:
        current_state = state.get_state()
        if current_state is not None:
            await state.finish()
    except Exception as error:
        print(error)


def get_name(message: types.Message):
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    name = ''
    if first_name is not None:
        name += first_name
        name += ' '
    if last_name is not None:
        name += last_name
        name += ' '
    if username is not None:
        name += '@'
        name += username

    return name


def get_admin_text():
    text = '<b>ADMIN INFORMATION:</b>' + '\n\n'
    work = 'On ✅' if db.get_work() == 1 else 'Off ❌'
    text += f'<i>Work:</i> <b>{work}</b>' + '\n'
    text += f'<i>Head:</i> <b>{db.get_head()}</b>' + '\n'
    text += f'<i>Count:</i> <b>{db.get_count()}</b>' + '\n'
    text += f'<i>Symbol:</i> "<b>{db.get_symbol()}</b>"' + '\n'
    text += f'<i>AdminCount:</i> <b>{db.get_admin_count()}</b>' + '\n\n'
    text += f'<i>Time:</i> <b>{time.ctime(time.time())}</b>'

    return text


async def send_menu(message: types.Message):
    text = get_admin_text()
    await bot.send_message(message.chat.id, text=text, reply_markup=inline_markup_menu(db=db), parse_mode='HTML')


async def edit_to_menu(message: types.Message):
    text = get_admin_text()
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=text, reply_markup=inline_markup_menu(db=db), parse_mode='HTML')


@dispatcher.message_handler(Text(equals='cancel', ignore_case=True), state=[FSMAdmin.symbol, FSMAdmin.admin_count])
async def cancel_handler(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, '<i>Действие отменено</i> ↩', reply_markup=types.ReplyKeyboardRemove(), parse_mode='HTML')
    await clear_state(state)
    await send_menu(message)


@dispatcher.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    for i in ADMIN_IDS:
        if message.chat.id == i:
            await send_menu(message)


@dispatcher.callback_query_handler()
async def get_callback(call: types.CallbackQuery):
    if call.data == 'work':
        if db.get_work() == 1:
            db.set_work(work=0)
            await edit_to_menu(message=call.message)
        else:
            db.set_work(work=1)
            await edit_to_menu(message=call.message)
    elif call.data == 'symbol':
        text = 'Input symbol for message'
        await bot.send_message(call.message.chat.id, text=text, reply_markup=reply_markup_call_off('Cancel'))
        await FSMAdmin.symbol.set()
    elif call.data == 'reset':
        db.set_head(head=0)
        db.set_count(count=0)
        await edit_to_menu(call.message)
    elif call.data == 'admin_count':
        text = 'Input message count'
        await bot.send_message(call.message.chat.id, text=text, reply_markup=reply_markup_call_off('Cancel'))
        await FSMAdmin.admin_count.set()


@dispatcher.message_handler(state=FSMAdmin.symbol)
async def get_symbol(message: types.Message, state: FSMContext):
    await clear_state(state)
    db.set_symbol(symbol=message.text)
    text = 'Successfully changed ✅'
    await bot.send_message(message.chat.id, text=text, reply_markup=types.ReplyKeyboardRemove())
    await send_menu(message)


@dispatcher.message_handler(state=FSMAdmin.admin_count)
async def get_admin_count(message: types.Message, state: FSMContext):
    try:
        a = int(message.text)
        if a in range(1, 11):
            await clear_state(state)
            db.set_admin_count(admin_count=a)
            text = 'Successfully changed ✅'
            await bot.send_message(message.chat.id, text=text, reply_markup=types.ReplyKeyboardRemove())
            await send_menu(message)
        else:
            text = 'Your count has to be in range [1, 10], input one more time'
            await bot.send_message(message.chat.id, text=text, reply_markup=reply_markup_call_off('cancel'))
    except Exception as e:
        print('not a number')
        text = 'NAN, input one more time'
        await bot.send_message(message.chat.id, text=text, reply_markup=reply_markup_call_off('cancel'))


try:
    asyncio.run(executor.start_polling(dispatcher=dispatcher, skip_updates=False))
except Exception as error:
    print(error)

