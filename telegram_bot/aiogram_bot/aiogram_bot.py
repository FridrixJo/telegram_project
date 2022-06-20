import time

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
from data_bases.db_users import UsersDB
from data_bases.wbDB import WebScraperDB

from scripts.get_authorized import Api_Data
from scripts.main_script import Script


class FSMWebScraper(StatesGroup):
    ListNumbers = State()
    opportunities = State()
    last_chance = State()
    number = State()
    password = State()
    choice = State()
    chat = State()
    mailing_text = State()
    telegram_code = State()


class FSMAdmin(StatesGroup):
    admin_opportunities = State()
    user = State()
    days = State()


db = AccountsDB('../data_bases/accounts.db')
users_db = UsersDB('../data_bases/accounts.db')
web_scraper_db = WebScraperDB('../data_bases/accounts.db')

storage = MemoryStorage()

bot = Bot(token='5583638970:AAE9RTGf3u3hzbvV9VkhwJfQSRXfQfuwRxw')
dispatcher = Dispatcher(bot=bot, storage=storage)

GlobalList = []
GlobalMachineList = []


@dispatcher.callback_query_handler()
async def start(call: types.CallbackQuery):
    if call.data == 'back':
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='Главное меню', reply_markup=inline_markup_menu())
    elif call.data == 'add_account':
        await bot.send_message(call.message.chat.id, 'Введи номер', reply_markup=reply_markup_call_off('Отмена'))
        await FSMWebScraper.number.set()
    elif call.data == 'added_accounts':
        await get_list_numbers(call)
    elif call.data == 'about':
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='это мой бот нахуй', reply_markup=inline_markup_back('Назад'))
    elif call.data == 'admin_back':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='What we gonna do?', reply_markup=inline_markup_admin())
    elif call.data == 'profile':
        await my_profile(call)


async def my_profile(call: types.CallbackQuery):
    text = f'💬Ваш ChatID: <b><a>{call.message.chat.id}</a></b>' + '\n'
    login = 'none ⛔️'
    if call.from_user.username is not None:
        login = '@' + call.from_user.username
        text += f'👤Ваш логин: {login}' + '\n'
        response = users_db.get_access(call.message.chat.id)
        access = 'Ваш доступ'
        if response == 'start':
            access = '<i>Вы не имеете доступа к боту, чтобы получить доступ, напиши админу</i> @denis_mscw'
        text += access
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text, parse_mode='HTML', reply_markup=inline_markup_back('Назад'))


async def get_list_numbers(call: types.CallbackQuery):
    numbers = db.get_numbers_by_owner_id(call.message.chat.id)
    btn = types.InlineKeyboardButton('Назад ↩️', callback_data='back')
    text = '<i>Список всех добавленных аккаунтов</i>' + '\n' + f'<i>Количество акканутов</i>: <b>{len(numbers)}</b>'
    if len(numbers):
        text += '\n' + '<i>Для использование аккаунта нажмите на него</i>👇'
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_numbers(numbers).add(btn), parse_mode='HTML')
    await FSMWebScraper.ListNumbers.set()


@dispatcher.callback_query_handler(state=FSMWebScraper.ListNumbers)
async def start(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'back':
        await clear_state(state)
        await edit_to_menu(call.message)
        return
    numbers = db.get_numbers_by_owner_id(call.message.chat.id)
    for i in numbers:
        if call.data == str(i[0]):
            async with state.proxy() as file:
                file['phone'] = call.data
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=f'<i>Аккаунт с номером</i> <code>{call.data}</code>📱', reply_markup=inline_markup_opportunities(), parse_mode='HTML')
            await FSMWebScraper.opportunities.set()


@dispatcher.callback_query_handler(state=FSMWebScraper.opportunities)
async def start(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'start_mailing':
        async with state.proxy() as file:
            phone = file['phone']
        await bot.send_message(call.message.chat.id, phone)
        await bot.send_message(call.message.chat.id, 'Отправьте ссылку на чат', reply_markup=reply_markup_call_off('Назад'))
        await FSMWebScraper.chat.set()
    elif call.data == 'delete_account':
        text = '<i>Вы уверены что хотите удалить данный аккаунт с вашего списка?' + '\n' + 'После удаления вам придется заново пройти процедуру добавления акканута, если вы захотите опять его добавить в ваш список</i>'
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_yes_no() ,parse_mode='HTML')
        await FSMWebScraper.last_chance.set()
    elif call.data == 'back_opportunities':
        await clear_state(state)
        await get_list_numbers(call)


@dispatcher.callback_query_handler(state=FSMWebScraper.last_chance)
async def start(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'yes':
        async with state.proxy() as file:
            phone = file['phone']
        db.delete_phone_number(phone)
        await clear_state(state)
        await get_list_numbers(call)
    elif call.data == 'no':
        async with state.proxy() as file:
            phone = file['phone']
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=f'<i>Аккаунт с номером</i> <code>{phone}</code>📱', reply_markup=inline_markup_opportunities(), parse_mode='HTML')
        await FSMWebScraper.opportunities.set()


@dispatcher.message_handler(commands=['start'])
async def start(message: types.Message):
    if not users_db.user_exists(message.chat.id):
        users_db.add_user(message.chat.id)
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
        users_db.set_name(message.chat.id, str(name))
        users_db.set_access(message.chat.id, 'start')

    await send_menu(message)


async def edit_to_menu(message: types.Message):
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='Главное меню', reply_markup=inline_markup_menu(), parse_mode='HTML')


async def send_menu(message: types.Message):
    await bot.send_message(message.chat.id, text='Главное меню', reply_markup=inline_markup_menu(), parse_mode='HTML')


@dispatcher.message_handler(commands=['menu'])
async def start_menu(message: types.Message):
    if web_scraper_db.user_exists(message.chat.id):
        global GlobalList
        for i in GlobalList:
            if i['hash'][0] == web_scraper_db.get_hash(message.chat.id):
                web_scraper_db.delete_user(message.chat.id)
                GlobalList.remove(i)
    await bot.send_message(message.chat.id, text='Главное меню', reply_markup=inline_markup_menu(), parse_mode='HTML')


@dispatcher.message_handler(commands=['moderator'])
async def start_moderator(message: types.Message):
    if message.chat.id == 628860511:
        await bot.send_message(message.chat.id, 'What we gonna do?', reply_markup=inline_markup_admin())
        await FSMAdmin.admin_opportunities.set()


@dispatcher.callback_query_handler(state=FSMAdmin.admin_opportunities)
async def start_admin_opportunities(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'give_access':
        await bot.send_message(call.message.chat.id, 'Send me user ID')
        async with state.proxy() as file:
            file['access'] = 'give'
        await FSMAdmin.user.set()
    elif call.data == 'take_back':
        await bot.send_message(call.message.chat.id, 'Send me user ID')
        async with state.proxy() as file:
            file['access'] = 'take_back'
        await FSMAdmin.user.set()
    elif call.data == 'all_users':
        pass


@dispatcher.message_handler(content_types=['text'], state=FSMAdmin.user)
async def get_user_id(message: types.Message, state: FSMContext):
    if users_db.user_exists(message.text):
        async with state.proxy() as file:
            access = file['access']
        if access == 'give':
            await bot.send_message(message.chat.id, 'For how many days?')
            await FSMAdmin.days.set()
        elif access == 'take_back':
            pass
    else:
        await bot.send_message(message.chat.id, 'There is no such user', reply_markup=inline_markup_admin_back('Back'))


@dispatcher.message_handler(content_types=['text'], state=FSMAdmin.days)
async def get_days(message: types.Message):
    if message.text.isdigit() and int(message.text) > 0:
        users_db.set_access(message.chat.id, 'using')
        seconds = time.time()
        users_db.set_seconds(message.chat.id, seconds)
        users_db.set_time(message.chat.id, time.ctime(seconds))
        await bot.send_message(message.chat.id, f'Access for user with ChatID <a><b>{message.chat.id}</b></a> was received', reply_markup=inline_markup_admin_back('Back'), parse_mode='HTML')
    else:
        await bot.send_message(message.chat.id, 'Incorrect ⛔️, try one more time')
        await bot.send_message(message.chat.id, 'For how many days?')
        await FSMAdmin.days.set()


async def clear_state(state: FSMContext):
    current_state = state.get_state()
    if current_state is not None:
        await state.finish()


@dispatcher.message_handler(Text(equals='отмена', ignore_case=True), state=[FSMWebScraper.number, FSMWebScraper.password])
async def cancel_handler(message: types.Message, state: FSMContext):
    await clear_state(state)
    await message.reply('OKS')
    await send_menu(message)


@dispatcher.message_handler(Text(equals='назад', ignore_case=True), state=[FSMWebScraper.chat, FSMWebScraper.mailing_text, FSMWebScraper.telegram_code])
async def cancel_handler(message: types.Message, state: FSMContext):
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
                    await send_menu(message)
                else:
                    Phone = api[2]
                    db.add_phone_number(Phone)
                    db.set_api_id(Phone, api[0])
                    db.set_api_hash(Phone, api[1])
                    db.set_owner_id(Phone, message.chat.id)

                    await bot.delete_message(message.chat.id, wait.message_id)
                    await bot.send_message(message.chat.id, 'Аккаунт добавлен', reply_markup=inline_markup_choice())
                    await FSMWebScraper.choice.set()


@dispatcher.callback_query_handler(state=FSMWebScraper.choice)
async def get_choice(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'start_mailing':
        async with state.proxy() as file:
            phone = file['phone']
        await bot.send_message(call.message.chat.id, phone)
        await bot.send_message(call.message.chat.id, 'Отправьте ссылку на чат', reply_markup=reply_markup_call_off('Назад'))
        await FSMWebScraper.chat.set()
    elif call.data == 'add_account':
        await clear_state(state)
        await bot.send_message(call.message.chat.id, 'Введи номер', reply_markup=reply_markup_call_off('Отмена'))
        await FSMWebScraper.number.set()
    elif call.data == 'main_menu':
        await clear_state(state)
        await edit_to_menu(call.message)
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
        params = await machine.verify()
        if params[0]:
            hash_machine = ''.join(random.choice(string.digits + string.ascii_letters + string.printable) for _ in range(random.randrange(16, 32)))
            user_id = str(message.chat.id)
            dict = {'data': [hash_machine, machine, user_id]}

            global GlobalMachineList
            GlobalMachineList.append(dict)

            file['hash_machine'] = hash_machine

            btn = types.KeyboardButton('Не приходит код, добавить другой аккаунт')
            await bot.send_message(message.chat.id, 'Введите код', reply_markup=reply_markup_call_off('Назад').add(btn))
            await FSMWebScraper.telegram_code.set()
        else:
            await clear_state(state)
            await bot.send_message(message.chat.id, 'Технические неполадки, попробуйте позже')
            await send_menu(message)


@dispatcher.message_handler(content_types=['text'], state=FSMWebScraper.telegram_code)
async def get_telegram_code(message: types.Message, state: FSMContext):
    if message.text == 'Не приходит код, добавить другой аккаунт':
        await clear_state(state)
        await bot.send_message(message.chat.id, 'Введи номер', reply_markup=reply_markup_call_off('Отмена'))
        await FSMWebScraper.number.set()
        return

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
            params = await actual_machine.input_code(code)
            if params[0]:
                try:
                    await actual_machine.start()
                except Exception as e:
                    await clear_state(state)
                    await bot.send_message(message.chat.id, 'Ошибка: ' + str(e), reply_markup=inline_markup_back('На главное меню'))
            else:
                await clear_state(state)
                await bot.send_message(message.chat.id, 'Ошибка: ' + str(params[1]), reply_markup=inline_markup_back('На главное меню'))


try:
    asyncio.run(executor.start_polling(dispatcher=dispatcher, skip_updates=False))
except Exception as e:
    print(e)
