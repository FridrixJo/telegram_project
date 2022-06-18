from aiogram import Bot, types
from aiogram import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text

from key_boards import *

import asyncio

import random
import string

from data_bases.db import AccountsDB
from data_bases.users import UsersDB
from data_bases.wbDB import WebScraperDB

from scripts.get_authorized import Api_Data
from scripts.main_script import Script


class FSMWebScraper(StatesGroup):
    ListNumbers = State()
    number = State()
    password = State()
    choice = State()
    chat = State()
    mailing_text = State()
    telegram_code = State()


db = AccountsDB('../data_bases/accounts.db')
users_db = UsersDB('../data_bases/accounts.db')
web_scraper_db = WebScraperDB('../data_bases/accounts.db')

storage = MemoryStorage()

bot = Bot(token='5583638970:AAE9RTGf3u3hzbvV9VkhwJfQSRXfQfuwRxw')
dispatcher = Dispatcher(bot=bot, storage=storage)

GlobalList = []
GlobalMachineList = []


async def menu(message: types.Message):
    await bot.send_message(message.chat.id, 'Главное меню', reply_markup=inline_markup_menu())


@dispatcher.callback_query_handler()
async def start(call: types.CallbackQuery):
    if call.data == 'back':
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='Главное меню', reply_markup=inline_markup_menu())
    elif call.data == 'add_account':
        await bot.send_message(call.message.chat.id, 'Введи номер', reply_markup=reply_markup_call_off('Отмена'))
        await FSMWebScraper.number.set()
    elif call.data == 'added_accounts':
        numbers = db.get_numbers_by_owner_id(call.message.chat.id)
        btn = types.InlineKeyboardButton('Назад', callback_data='back')
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='Список всех активных аккаунтов', reply_markup=inline_markup_numbers(numbers).add(btn))
        await FSMWebScraper.ListNumbers.set()
    elif call.data == 'about':
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)


@dispatcher.callback_query_handler(state=FSMWebScraper.ListNumbers)
async def start(call: types.CallbackQuery, state: FSMContext):
    numbers = db.get_numbers_by_owner_id(call.message.chat.id)
    for i in numbers:
        if call.data == str(i[0]):
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            async with state.proxy() as file:
                file['phone'] = call.data
            await bot.send_message(call.message.chat.id, 'Выберите', reply_markup=inline_markup_choice())
            await FSMWebScraper.choice.set()


@dispatcher.message_handler(commands=['menu'])
async def menu(message: types.Message):
    if web_scraper_db.user_exists(message.chat.id):
        global GlobalList
        for i in GlobalList:
            if i['hash'][0] == web_scraper_db.get_hash(message.chat.id):
                web_scraper_db.delete_user(message.chat.id)
                GlobalList.remove(i)
    await bot.send_message(message.chat.id, 'Главное меню', reply_markup=inline_markup_menu())


@dispatcher.message_handler(Text(equals='отмена', ignore_case=True), state=[FSMWebScraper.number, FSMWebScraper.password])
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OKS')
    await menu(message)


@dispatcher.message_handler(Text(equals='назад', ignore_case=True), state=[FSMWebScraper.chat, FSMWebScraper.mailing_text, FSMWebScraper.telegram_code])
async def cancle_handler(message: types.Message, state: FSMContext):
    current_state = state.get_state()
    await message.reply('OKS')
    await bot.send_message(message.chat.id, 'Выберите одно из 3', reply_markup=inline_markup_choice())
    await FSMWebScraper.choice.set()


@dispatcher.message_handler(content_types=['text'], state=FSMWebScraper.number)
async def get_number(message: types.Message, state: FSMContext):
    wait = await bot.send_message(message.chat.id, 'Ожидайте')
    if '+' in message.text:

        async with state.proxy() as file:
            file['phone'] = message.text

        async with state.proxy() as file:
            Phone = file['phone']

        if db.account_exists(Phone):
            await bot.delete_message(message.chat.id, wait.message_id)
            await bot.send_message(message.chat.id, 'Аккаунт уже добавлен', reply_markup=inline_markup_choice())
            await FSMWebScraper.choice.set()
        else:
            scraper = Api_Data(Phone)

            params = await scraper.login()
            if params[0]:
                hash = ''.join(random.choice(string.digits + string.ascii_letters) for _ in range(random.randrange(16, 32)))
                user_id = str(message.chat.id)
                dict = {'data': [hash, scraper, user_id]}

                web_scraper_db.add_user(message.chat.id)
                await asyncio.sleep(1)
                web_scraper_db.set_web_scraper_id(message.chat.id, str(scraper))
                web_scraper_db.set_hash(message.chat.id, hash)

                global GlobalList
                GlobalList.append(dict)

                async with state.proxy() as file:
                    file['hash'] = hash

                await bot.delete_message(message.chat.id, wait.message_id)
                await bot.send_message(message.chat.id, 'Введи код', reply_markup=reply_markup_call_off('Отмена'))
                await FSMWebScraper.password.set()
            else:
                await bot.delete_message(message.chat.id, wait.message_id)
                await bot.send_message(message.chat.id, 'Некорректный номер')
                await bot.send_message(message.chat.id, 'Введи номер еще раз', reply_markup=reply_markup_call_off('Отмена'))
                await FSMWebScraper.number.set()
    else:
        await bot.delete_message(message.chat.id, wait.message_id)
        await bot.send_message(message.chat.id, 'Введи номер', reply_markup=reply_markup_call_off('Отмена'))
        await FSMWebScraper.number.set()


@dispatcher.message_handler(content_types=['text'], state=FSMWebScraper.password)
async def get_password(message: types.Message, state: FSMContext):
    wait = await bot.send_message(message.chat.id, 'Ожидайте')
    async with state.proxy() as file:
        file['password'] = message.text

    async with state.proxy() as file:
        password = file['password']
        hash = file['hash']

    global GlobalList
    actual_browser: Api_Data

    for i in GlobalList:
        if i['data'][0] == hash:
            actual_browser = i['data'][1]
            params = await actual_browser.input_password(password)
            if not params[0]:
                await actual_browser.remove_error()
                await bot.delete_message(message.chat.id, wait.message_id)
                await bot.send_message(message.chat.id, 'Невереный код, введи еще раз', reply_markup=reply_markup_call_off('Отмена'))
                await FSMWebScraper.password.set()
            else:
                api = await actual_browser.getting_data()

                web_scraper_db.delete_user(message.chat.id)
                GlobalList.remove(i)

                if not api[3]:
                    await bot.delete_message(message.chat.id, wait.message_id)
                    await bot.send_message(message.chat.id, 'Попробуйте позже или добавьте другой аккаунт')
                    await menu(message)
                else:
                    Phone = api[2]
                    db.add_phone_number(Phone)
                    db.set_api_id(Phone, api[0])
                    db.set_api_hash(Phone, api[1])
                    db.set_owner_id(Phone, message.chat.id)

                    await bot.delete_message(message.chat.id, wait.message_id)
                    await bot.send_message(message.chat.id, 'Аккаунт добавлен', reply_markup=inline_markup_choice())
                    await FSMWebScraper.choice.set()

    await asyncio.sleep(1)


@dispatcher.callback_query_handler(state=FSMWebScraper.choice)
async def get_choice(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'start_mailing':
        async with state.proxy() as file:
            phone = file['phone']

        await bot.send_message(call.message.chat.id, phone)

        await bot.send_message(call.message.chat.id, phone)
        await bot.send_message(call.message.chat.id, 'Отправьте ссылку на чат', reply_markup=reply_markup_call_off('Назад'))
        await FSMWebScraper.chat.set()
    elif call.data == 'add_account':
        current_state = state.get_state()
        if current_state is None:
            return
        await state.finish()
        await bot.send_message(call.message.chat.id, 'Введи номер', reply_markup=reply_markup_call_off('Отмена'))
        await FSMWebScraper.number.set()
    elif call.data == 'main_menu':
        current_state = state.get_state()
        if current_state is None:
            return
        await state.finish()
        await menu(call.message)
    else:
        await bot.send_message(call.message.chat.id, 'Выберите одно из 3')
        await FSMWebScraper.choice.set()


@dispatcher.message_handler(content_types=['text'], state=FSMWebScraper.chat)
async def get_chat(message: types.Message, state: FSMContext):
    async with state.proxy() as file:
        file['chat'] = message.text
        await bot.send_message(message.chat.id, file['chat'])
    await bot.send_message(message.chat.id, 'Отправьте сообщение для рассылки', reply_markup=reply_markup_call_off('Назад'))
    await FSMWebScraper.mailing_text.set()


@dispatcher.message_handler(content_types=['text'], state=FSMWebScraper.mailing_text)
async def get_mailing_text(message: types.Message, state: FSMContext):
    async with state.proxy() as file:
        file['mailing_text'] = message.text
        phone = file['phone']
        machine = Script(session_name=phone,
                         api_id=db.get_api_id(phone),
                         api_hash=db.get_api_hash(phone),
                         phone_number=phone,
                         chat_link=file['chat'],
                         data=file['mailing_text'])
        await bot.send_message(message.chat.id, 'Отправляем код')
        if await machine.verify():
            hash_machine = ''.join(random.choice(string.digits + string.ascii_letters + string.printable) for _ in range(random.randrange(16, 32)))
            user_id = str(message.chat.id)
            dict = {'data': [hash_machine, machine, user_id]}

            global GlobalMachineList
            GlobalMachineList.append(dict)

            file['hash_machine'] = hash_machine

            await bot.send_message(message.chat.id, 'Введите код', reply_markup=reply_markup_call_off('Назад'))
            await FSMWebScraper.telegram_code.set()


@dispatcher.message_handler(content_types=['text'], state=FSMWebScraper.telegram_code)
async def get_telegram_code(message: types.Message, state: FSMContext):
    wait = await bot.send_message(message.chat.id, 'Ожидайте')
    async with state.proxy() as file:
        file['code'] = message.text

    async with state.proxy() as file:
        code = file['code']
        hash_machine = file['hash_machine']

    global GlobalMachineList
    actual_machine: Script

    for i in GlobalMachineList:
        if i['data'][0] == hash_machine:
            actual_machine = i['data'][1]
            await actual_machine.input_code(code)
            await actual_machine.start()


try:
    asyncio.run(executor.start_polling(dispatcher=dispatcher, skip_updates=False))
except Exception as e:
    print(e)
