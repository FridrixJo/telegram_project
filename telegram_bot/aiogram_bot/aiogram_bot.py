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
from data_bases.machineDB import MachineDB

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
    choose_user = State()
    numbers_or_back = State()
    choose_phone = State()
    phone_info_back = State()
    admin_opportunities = State()
    cancel = State()
    user = State()
    days = State()
    period_list = State()
    del_param = State()
    sharing = State()
    statistics = State()


db = AccountsDB('../data_bases/accounts.db')
users_db = UsersDB('../data_bases/accounts.db')
web_scraper_db = WebScraperDB('../data_bases/accounts.db')
machine_db = MachineDB('../data_bases/accounts.db')

storage = MemoryStorage()

bot = Bot(token='5583638970:AAE9RTGf3u3hzbvV9VkhwJfQSRXfQfuwRxw')
dispatcher = Dispatcher(bot=bot, storage=storage)

GlobalList = []
GlobalMachineList = []


# MAIN MENU CALLBACK_QUERY_HANDLER

@dispatcher.callback_query_handler()
async def start(call: types.CallbackQuery):
    if call.data == 'back':
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='Главное меню', reply_markup=inline_markup_menu())
    elif call.data == 'add_account':
        if users_db.get_access(call.message.chat.id) == 'using':
            await bot.send_message(call.message.chat.id, '🔹Введи номер аккаунта Telegram ☎\nНомер формата <b>+7YYYXXXXXXX</b>, или формата любой другой страны\n<b>🔺Примечание:</b> знак ➕ должен обязательно находиться вначале номера', reply_markup=reply_markup_call_off('Отмена'), parse_mode='HTML')
            await FSMWebScraper.number.set()
        else:
            text = '<i>Вы не имеет доступ к боту ⛔️\nДля получения доступа напишите админу</i> <b>@denis_mscw</b> 👨‍💻'
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_back('Назад'), parse_mode='HTML')

    elif call.data == 'added_accounts':
        if users_db.get_access(call.message.chat.id) == 'using':
            await get_list_numbers(call)
            await FSMWebScraper.ListNumbers.set()
        else:
            text = '<i>Вы не имеет доступ к боту ⛔️\nДля получения доступа напишите админу</i> <b>@denis_mscw</b> 👨‍💻'
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_back('Назад'), parse_mode='HTML')
    elif call.data == 'ok':
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    elif call.data == 'about':
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='это мой бот нахуй', reply_markup=inline_markup_back('Назад'))
    elif call.data == 'profile':
        await my_profile(call)


# BACK MESSAGE_HANDLER

@dispatcher.message_handler(Text(equals='отмена', ignore_case=True), state=[FSMWebScraper.number, FSMWebScraper.password])
async def cancel_handler(message: types.Message, state: FSMContext):
    if web_scraper_db.user_exists(message.chat.id):
        web_scraper_db.delete_user(message.chat.id)
        global GlobalList
        hash_scraper = web_scraper_db.get_hash(message.chat.id)
        for i in GlobalList:
            if i['data'][0] == hash_scraper:
                GlobalList.remove(i)
    await clear_state(state)
    await bot.send_message(message.chat.id, '<i>Действие отменено</i> ↩', reply_markup=types.ReplyKeyboardRemove(), parse_mode='HTML')
    await send_menu(message)


@dispatcher.message_handler(Text(equals='назад', ignore_case=True), state=[FSMWebScraper.chat, FSMWebScraper.mailing_text, FSMWebScraper.telegram_code])
async def cancel_handler(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, '<i>Действие отменено</i> ↩', reply_markup=types.ReplyKeyboardRemove(), parse_mode='HTML')
    async with state.proxy() as file:
        phone = file['phone']
    await bot.send_message(chat_id=message.chat.id, text=f'<i>Аккаунт с номером</i> <code>{phone}</code>📱', reply_markup=inline_markup_opportunities(), parse_mode='HTML')
    await FSMWebScraper.opportunities.set()


@dispatcher.callback_query_handler(state=FSMAdmin.cancel)
async def admin_back(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'admin_back':
        await clear_state(state)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='<i>What we gonna do machineglytkelly👨‍💻</i>?', reply_markup=inline_markup_admin(), parse_mode='HTML')
        await FSMAdmin.admin_opportunities.set()


async def my_profile(call: types.CallbackQuery):
    text = f'💬Ваш ChatID: <b><code>{call.message.chat.id}</code></b>' + '\n'
    login = 'none ⛔️'
    if call.from_user.username is not None:
        login = '@' + call.from_user.username
    text += f'👤Ваш логин: {login}' + '\n'
    response = users_db.get_access(call.message.chat.id)
    access = '<i>🙅‍♂️Вы не имеете доступа к боту, чтобы получить доступ, напишите админу</i> <b>@denis_mscw</b> 👨‍💻'
    if response == 'using':
        seconds = users_db.get_seconds(call.message.chat.id)
        period = users_db.get_period(call.message.chat.id) * 24 * 3600
        print(seconds, period)
        access = f'<i>🗓Вы имеете доступ к боту до <b>{time.ctime(seconds + period)}</b></i>'
    text += access
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text, parse_mode='HTML', reply_markup=inline_markup_back('Назад'))


async def get_list_numbers(call: types.CallbackQuery):
    numbers = db.get_added_numbers_by_owner_id(call.message.chat.id, 'added')
    btn = types.InlineKeyboardButton('Назад ↩️', callback_data='back')
    text = '<i>Список всех добавленных аккаунтов</i>' + '\n' + f'<i>Количество акканутов</i>: <b>{len(numbers)}</b>'
    if len(numbers):
        text += '\n' + '<i>Для использование аккаунта нажмите на него</i>👇'
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_numbers(numbers, db).add(btn), parse_mode='HTML')


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
        if db.get_condition(phone) == 0:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            await bot.send_message(call.message.chat.id, phone)
            await bot.send_message(call.message.chat.id, '<i>Отправьте ссылку на чат</i> 🔗', reply_markup=reply_markup_call_off('Назад'), parse_mode='HTML')
            await FSMWebScraper.chat.set()
        else:
            await clear_state(state)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Бот уже запущен на этом аккаунте, выберите другой', reply_markup=inline_markup_back('Главное меню'))
    elif call.data == 'delete_account':
        text = '<i>Вы уверены что хотите удалить данный аккаунт с вашего списка?' + '\n' + 'После удаления вам придется заново пройти процедуру добавления акканута, если вы захотите опять его добавить в свой список</i>'
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_yes_no(), parse_mode='HTML')
        await FSMWebScraper.last_chance.set()
    elif call.data == 'back_opportunities':
        await clear_state(state)
        await get_list_numbers(call)
        await FSMWebScraper.ListNumbers.set()


@dispatcher.callback_query_handler(state=FSMWebScraper.last_chance)
async def start(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as file:
        phone = file['phone']
    if call.data == 'yes':
        db.set_status(phone, 'deleted')
        await clear_state(state)
        await get_list_numbers(call)
    elif call.data == 'no':
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=f'<i>Аккаунт с номером</i> <code>{phone}</code>📱', reply_markup=inline_markup_opportunities(), parse_mode='HTML')
        await FSMWebScraper.opportunities.set()


async def edit_to_menu(message: types.Message):
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='Главное меню', reply_markup=inline_markup_menu())


async def send_menu(message: types.Message):
    await bot.send_message(message.chat.id, text='Главное меню', reply_markup=inline_markup_menu())


# BOT COMMANDS

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


@dispatcher.message_handler(commands=['menu'], state=['*'])
async def start_menu(message: types.Message, state: FSMContext):
    global GlobalList, GlobalMachineList
    if web_scraper_db.user_exists(message.chat.id):
        await clear_state(state)
        for i in GlobalList:
            if i['data'][0] == web_scraper_db.get_hash(message.chat.id):
                web_scraper_db.delete_user(message.chat.id)
                GlobalList.remove(i)
    if machine_db.user_exists(message.chat.id):
        await clear_state(state)
        for i in GlobalMachineList:
            if i['data'][0] == machine_db.get_hash(message.chat.id):
                machine_db.delete_user(message.chat.id)
                GlobalMachineList.remove(i)
    await bot.send_message(message.chat.id, text='Главное меню', reply_markup=inline_markup_menu(), parse_mode='HTML')


async def clear_state(state: FSMContext):
    try:
        current_state = state.get_state()
        if current_state is not None:
            await state.finish()
    except Exception as error:
        print(error)


# GET NUMBER # WEB_SCRAPER

@dispatcher.message_handler(content_types=['text'], state=FSMWebScraper.number)
async def get_number(message: types.Message, state: FSMContext):
    wait = await bot.send_message(message.chat.id, '<i>Ожидайте</i> ⏳', reply_markup=types.ReplyKeyboardRemove(), parse_mode='HTML')
    if '+' in message.text:

        async with state.proxy() as file:
            file['phone'] = message.text
            phone = message.text

        if db.account_exists(phone):
            db.set_status(phone, 'added')
            await bot.delete_message(message.chat.id, wait.message_id)
            await bot.send_message(message.chat.id, '<i>Аккаунт уже добавлен</i> 🧩', reply_markup=inline_markup_choice(), parse_mode='HTML')
            await FSMWebScraper.choice.set()
        else:
            scraper = Api_Data(phone)

            params = await scraper.login()
            if params[0]:
                hash_scraper = ''.join(random.choice(string.digits + string.ascii_letters) for _ in range(random.randrange(16, 32)))
                user_id = message.chat.id
                web_dict = {'data': [hash_scraper, scraper, user_id]}

                web_scraper_db.add_user(message.chat.id)
                await asyncio.sleep(1)
                web_scraper_db.set_web_scraper_id(message.chat.id, str(scraper))
                web_scraper_db.set_hash(message.chat.id, hash_scraper)

                global GlobalList
                GlobalList.append(web_dict)

                async with state.proxy() as file:
                    file['hash_scraper'] = hash_scraper

                await bot.delete_message(message.chat.id, wait.message_id)
                await bot.send_message(message.chat.id, '🔹Введи код, отправленный вам в Telegram 🔤', reply_markup=reply_markup_call_off('Отмена'))
                await FSMWebScraper.password.set()
            else:
                await scraper.remove_error()
                await bot.delete_message(message.chat.id, wait.message_id)
                await bot.send_message(message.chat.id, '⛔<b>Введенный вами номер некорректен, повторите процедуру еще раз</b>', parse_mode='HTML')
                await bot.send_message(message.chat.id, '🔹Введи номер аккаунта Telegram ☎\nНомер формата <b>+7YYYXXXXXXX</b>, или формата любой другой страны\n<b>🔺Примечание:</b> знак ➕ должен обязательно находиться вначале номера', reply_markup=reply_markup_call_off('Отмена'), parse_mode='HTML')
                await FSMWebScraper.number.set()

    else:
        await bot.delete_message(message.chat.id, wait.message_id)
        await bot.send_message(message.chat.id, '⛔<b>Введенный вами номер некорректен (знак ➕ должен обязательно находиться вначале номера), повторите процедуру еще раз</b>', parse_mode='HTML')
        await bot.send_message(message.chat.id, '🔹Введи номер аккаунта Telegram ☎\nНомер формата <b>+7YYYXXXXXXX</b>, или формата любой другой страны\n<b>🔺Примечание:</b> знак ➕ должен обязательно находиться вначале номера', reply_markup=reply_markup_call_off('Отмена'), parse_mode='HTML')
        await FSMWebScraper.number.set()


# GET PASSWORD WHEN REGISTER NEW ACCOUNT # WEB_SCRAPER

@dispatcher.message_handler(content_types=['text'], state=FSMWebScraper.password)
async def get_password(message: types.Message, state: FSMContext):
    wait = await bot.send_message(message.chat.id, '<i>Ожидайте</i> ⏳', reply_markup=types.ReplyKeyboardRemove(), parse_mode='HTML')

    async with state.proxy() as file:
        hash_scraper = file['hash_scraper']

    global GlobalList
    actual_browser: Api_Data

    for i in GlobalList:
        if i['data'][0] == hash_scraper:
            actual_browser = i['data'][1]
            params = await actual_browser.input_password(message.text)
            if not params[0]:
                await actual_browser.remove_error()
                await bot.delete_message(message.chat.id, wait.message_id)
                await bot.send_message(message.chat.id, '⛔<b>Неверный код, попробуйте ввести еще раз</b>', reply_markup=reply_markup_call_off('Отмена'), parse_mode='HTML')
                await FSMWebScraper.password.set()
            else:
                api = await actual_browser.getting_data()
                web_scraper_db.delete_user(message.chat.id)
                GlobalList.remove(i)
                if not api[3]:
                    await bot.delete_message(message.chat.id, wait.message_id)
                    await bot.send_message(message.chat.id, '<b>Технические неполадки</b> 🛠... <i>Попробуйте позже или добавьте другой аккаунт</i>', parse_mode='HTML')
                    await send_menu(message)
                else:
                    phone = api[2]
                    db.add_phone_number(phone)
                    db.set_api_id(phone, api[0])
                    db.set_api_hash(phone, api[1])
                    db.set_owner_id(phone, message.chat.id)

                    await bot.delete_message(message.chat.id, wait.message_id)
                    await bot.send_message(message.chat.id, '<i>Аккаунт успешно добавлен</i> 🧩', reply_markup=inline_markup_choice(), parse_mode='HTML')
                    await FSMWebScraper.choice.set()


# SUB MENU WHEN ADDING SUCCESS NEW NUMBER


@dispatcher.callback_query_handler(state=FSMWebScraper.choice)
async def get_choice(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'start_mailing':
        async with state.proxy() as file:
            phone = file['phone']
        if db.get_condition(phone) == 0:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            await bot.send_message(call.message.chat.id, phone)
            await bot.send_message(call.message.chat.id, '🔹Отправьте ссылку на чат 🔗', reply_markup=reply_markup_call_off('Назад'), parse_mode='HTML')
            await FSMWebScraper.chat.set()
        else:
            await clear_state(state)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='🚫<b>Бот уже запущен на этом аккаунте, выберите другой</b>', reply_markup=inline_markup_back('Главное меню'), parse_mode='HTML')

    elif call.data == 'add_account':
        await clear_state(state)
        await bot.send_message(call.message.chat.id, '🔹Введи номер аккаунта Telegram ☎\nНомер формата <b>+7YYYXXXXXXX</b>, или формата любой другой страны\n<b>🔺Примечание:</b> знак ➕ должен обязательно находиться вначале номера', reply_markup=reply_markup_call_off('Отмена'), parse_mode='HTML')
        await FSMWebScraper.number.set()
    elif call.data == 'main_menu':
        await clear_state(state)
        await send_menu(call.message)


# GET CHAT FOR PARSING

@dispatcher.message_handler(content_types=['text'], state=FSMWebScraper.chat)
async def get_chat(message: types.Message, state: FSMContext):
    async with state.proxy() as file:
        file['chat'] = message.text
    await bot.send_message(message.chat.id, '<i>Принято</i> ✅', reply_markup=types.ReplyKeyboardRemove(), parse_mode='HTML')
    await bot.send_message(message.chat.id, '🔹Отправьте сообщение для рассылки 📩', reply_markup=reply_markup_call_off('Назад'))
    await FSMWebScraper.mailing_text.set()


# GET TEXT TO MAILING

@dispatcher.message_handler(content_types=['text'], state=FSMWebScraper.mailing_text)
async def get_mailing_text(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, '<i>Принято</i> ✅', reply_markup=types.ReplyKeyboardRemove(), parse_mode='HTML')
    async with state.proxy() as file:
        file['mailing_text'] = message.text
        phone = file['phone']
        machine = Script(session_name=phone,
                         api_id=db.get_api_id(phone),
                         api_hash=db.get_api_hash(phone),
                         phone_number=phone,
                         chat_link=file['chat'],
                         data=message.text)
        db.set_mailing_message(phone, message.text)
        await bot.send_message(message.chat.id, '<i>Отправляем код в Telegram</i> ⏳', parse_mode='HTML')
        params = await machine.verify()
        if params[0]:
            hash_machine = ''.join(random.choice(string.digits + string.ascii_letters + string.printable) for _ in range(random.randrange(16, 32)))
            user_id = str(message.chat.id)
            dict_machine = {'data': [hash_machine, machine, user_id]}

            machine_db.add_user(message.chat.id)
            await asyncio.sleep(1)
            machine_db.set_machine_id(message.chat.id, str(machine))
            machine_db.set_hash(message.chat.id, hash_machine)

            global GlobalMachineList
            GlobalMachineList.append(dict_machine)

            file['hash_machine'] = hash_machine

            await bot.send_message(message.chat.id, '🔹Введите код, отправленный вам в Telegram 🔢', reply_markup=reply_markup_call_off('Не приходит код, вернуться на главное меню'))
            await FSMWebScraper.telegram_code.set()
        else:
            await clear_state(state)
            await clear_state(state)
            await bot.send_message(message.chat.id, '⛔<b>Ошибка:</b> ' + str(params[1]), reply_markup=inline_markup_back('На главное меню'), parse_mode='HTML')


# TELEGRAM_CODE FINAL PART

@dispatcher.message_handler(content_types=['text'], state=FSMWebScraper.telegram_code)
async def get_telegram_code(message: types.Message, state: FSMContext):
    global GlobalMachineList
    if message.text == 'Не приходит код, вернуться на главное меню':
        await bot.send_message(message.chat.id, '<i>Принято</i> ✅', reply_markup=types.ReplyKeyboardRemove(), parse_mode='HTML')
        await clear_state(state)
        if machine_db.user_exists(message.chat.id):
            hash_machine = machine_db.get_hash(message.chat.id)
            machine_db.delete_user(message.chat.id)
            for i in GlobalMachineList:
                if i['data'][0] == hash_machine:
                    GlobalMachineList.remove(i)
        await send_menu(message)
    else:
        wait = await bot.send_message(message.chat.id, '<i>Ожидайте</i> ⏳', reply_markup=types.ReplyKeyboardRemove(), parse_mode='HTML')

        async with state.proxy() as file:
            hash_machine = file['hash_machine']

        actual_machine: Script

        for i in GlobalMachineList:
            if i['data'][0] == hash_machine:
                actual_machine = i['data'][1]
                GlobalMachineList.remove(i)
                if machine_db.user_exists(message.chat.id):
                    machine_db.delete_user(message.chat.id)
                try:
                    params = await actual_machine.input_code(message.text)
                    if params[0]:
                        chat_params = await actual_machine.get_chat_members()
                        if chat_params[0]:
                            phone = actual_machine.get_phone()
                            db.set_chat(phone, actual_machine.get_chat_link())
                            db.set_condition(phone, True)
                            db.set_name(phone, await actual_machine.get_account_name())
                            db.set_username(phone, await actual_machine.get_account_username())
                            await clear_state(state)
                            await bot.delete_message(chat_id=message.chat.id, message_id=wait.message_id)
                            await bot.send_message(message.chat.id, 'Бот успешно запущен ✅', reply_markup=inline_markup_back('На главное меню'))
                            message_count = db.get_message_count(phone)
                            try:
                                writting_params = await actual_machine.write()
                                message_count += writting_params[0]
                                db.set_message_count(phone, message_count)
                                text = f'<i>🤖 Бот завершил работу\n на аккаунте</i> <code>{phone}</code> <b>{db.get_name(phone)} {db.get_username(phone)}</b>' + '\n'
                                text += f'<i>📤 Количество отправленных\n сообщений:</i> <b>{writting_params[0]}</b>'
                                db.set_condition(phone, False)
                                await bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=inline_markup_ok())
                            except Exception as error:
                                print(error)
                                db.set_condition(phone, False)
                                text = f'<i>🤖 Бот на аккаунте</i> <code>{phone}</code> <b>{db.get_name(phone)} {db.get_username(phone)}</b <i>приостановлен</i> 🚫'
                                await bot.send_message(message.chat.id, text, reply_markup=inline_markup_ok(), parse_mode='HTML')
                        else:
                            await clear_state(state)
                            await bot.send_message(message.chat.id, '⛔<b>Ошибка:</b> ' + str(chat_params[1]), reply_markup=inline_markup_back('На главное меню'), parse_mode='HTML')

                    else:
                        await clear_state(state)
                        await bot.send_message(message.chat.id, '⛔<b>Ошибка:</b> ' + str(params[1]), reply_markup=inline_markup_back('На главное меню'), parse_mode='HTML')
                except Exception as error:
                    await clear_state(state)
                    await bot.send_message(message.chat.id, '⛔<b>Ошибка:</b> ' + str(error), reply_markup=inline_markup_back('На главное меню'), parse_mode='HTML')

# MODERATOR PART


@dispatcher.message_handler(commands=['moderator'], state=['*'])
async def start_moderator(message: types.Message, state: FSMContext):
    await clear_state(state)
    if message.chat.id == 628860511 or message.chat.id == 899951880:
        await bot.send_message(message.chat.id, text='<i>What we gonna do machineglytkelly👨‍💻</i>?', reply_markup=inline_markup_admin(), parse_mode='HTML')
        await FSMAdmin.admin_opportunities.set()

# MODERATOR OPPORTUNITIES


@dispatcher.callback_query_handler(state=FSMAdmin.admin_opportunities)
async def start_admin_opportunities(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'give_access':
        await bot.send_message(call.message.chat.id, 'Send me user ID', reply_markup=reply_markup_call_off('Cancel'))
        async with state.proxy() as file:
            file['access'] = 'give'
        await FSMAdmin.user.set()
    elif call.data == 'take_back_access':
        await bot.send_message(call.message.chat.id, 'Send me user ID', reply_markup=reply_markup_call_off('Cancel'))
        async with state.proxy() as file:
            file['access'] = 'take_back'
        await FSMAdmin.user.set()
    elif call.data == 'all_users':
        await get_list_users(call)
        await FSMAdmin.choose_user.set()
    elif call.data == 'access_users':
        await get_list_using_users(call)
        await FSMAdmin.choose_user.set()
    elif call.data == 'main_menu':
        await clear_state(state)
        await edit_to_menu(call.message)
    elif call.data == 'del_func':
        await bot.send_message(call.message.chat.id, 'Input del_params', reply_markup=reply_markup_call_off('Cancel'))
        await FSMAdmin.del_param.set()
    elif call.data == 'period_list':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=str(users_db.get_periods()), reply_markup=inline_markup_admin_back('Back', 'admin_back'))
        await FSMAdmin.cancel.set()
    elif call.data == 'sharing':
        await bot.send_message(call.message.chat.id, 'Input data for sharing', reply_markup=reply_markup_call_off('Cancel'))
        await FSMAdmin.sharing.set()
    elif call.data == 'statistics':
        await clear_state(state)
        await get_statistics(call)
        await FSMAdmin.statistics.set()


@dispatcher.message_handler(state=FSMAdmin.del_param)
async def del_access(message: types.Message):
    users_by_period = users_db.get_users_by_period(message.text)
    await bot.send_message(message.chat.id, 'Ok', reply_markup=types.ReplyKeyboardRemove())
    text = 'Access was restricted on accounts with ChatID: \n'
    for i in users_by_period:
        if (users_db.get_seconds(i[0]) + users_db.get_period(i[0])*24*3600) - time.time() <= 0:
            users_db.set_access(i[0], 'start')
            users_db.set_seconds(i[0], None)
            users_db.set_time(i[0], None)
            users_db.set_period(i[0], None)
            text += f'<b>{i[0]}</b>' + '\n'
    await bot.send_message(message.chat.id, text=text, reply_markup=inline_markup_admin_back('Back', 'admin_back'), parse_mode='HTML')
    await FSMAdmin.cancel.set()


@dispatcher.message_handler(content_types=['text'], state=FSMAdmin.sharing)
async def start_sharing(message: types.Message, state: FSMContext):
    for i in users_db.get_users():
        try:
            await bot.send_message(i[0], message.text, reply_markup=inline_markup_ok())
        except Exception as error:
            print(error)
    await bot.send_message(message.chat.id, 'Done', reply_markup=types.ReplyKeyboardRemove())
    await start_moderator(message, state)


async def get_statistics(call):
    text = f'Users quantity: <b>{len(users_db.get_users())}</b>' + '\n'
    text += f'Numbers quantity: <b>{len(db.get_all_numbers())}</b>' + '\n'
    conditons = db.get_all_conditions()
    count = 0
    for i in conditons:
        if i[0] == 1:
            count += 1
    text += f'Active accounts quantity: <b>{count}</b>' + '\n'
    messages = db.get_all_message_count()
    all_message_cout = 0
    for i in messages:
        all_message_cout += i[0]
    text += f'All sent messages quantity: <b>{all_message_cout}</b>' + '\n'
    global GlobalList, GlobalMachineList
    text += f'GlobalList length: <b>{len(GlobalList)}</b>' + '\n'
    text += f'GlobalMachineList length: <b>{len(GlobalMachineList)}</b>' + '\n'
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_admin_back('Назад', 'admin_back'), parse_mode='HTML')


@dispatcher.callback_query_handler(state=FSMAdmin.statistics)
async def start(call: types.CallbackQuery):
    if call.data == 'admin_back':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='<i>What we gonna do machineglytkelly👨‍💻</i>?', reply_markup=inline_markup_admin(), parse_mode='HTML')
        await FSMAdmin.admin_opportunities.set()


async def get_list_users(call: types.CallbackQuery):
    users = []
    for i in users_db.get_users():
        user = []
        user.append(str(i[0]))
        user.append(str(users_db.get_name(i[0])))
        users.append(user)

    btn = types.InlineKeyboardButton('Back ↩️', callback_data='admin_back')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='List of all users', reply_markup=inline_markup_users(users).add(btn))


async def get_list_using_users(call: types.CallbackQuery):
    users = []
    for i in users_db.get_users_by_access('using'):
        user = []
        user.append(str(i[0]))
        user.append(str(users_db.get_name(i[0])))
        users.append(user)

    btn = types.InlineKeyboardButton('Back ↩️', callback_data='admin_back')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='List of all users with access to bot', reply_markup=inline_markup_users(users).add(btn))


@dispatcher.callback_query_handler(state=FSMAdmin.choose_user)
async def start(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'admin_back':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='<i>What we gonna do machineglytkelly👨‍💻</i>?', reply_markup=inline_markup_admin(), parse_mode='HTML')
        await clear_state(state)
        await FSMAdmin.admin_opportunities.set()
    else:
        for i in users_db.get_users():
            if str(i[0]) == call.data:
                user_id = str(i[0])
                response = f'user_id: {user_id}' + '\n'
                response += f'name: {users_db.get_name(user_id)}' + '\n'
                response += f'access: {users_db.get_time(user_id)}' + '\n'
                response += f'period: {users_db.get_period(user_id)}' + '\n'
                response += f'Numbers quantity: {len(db.get_numbers_by_owner_id(user_id))}' + '\n'
                response += f'Purchases: {users_db.get_purchases(user_id)}' + '\n'
                message_count = db.get_all_message_count_by_user_id(user_id)
                count = 0
                for j in message_count:
                    count += j[0]
                response += f'Message count: {count}'

                async with state.proxy() as file:
                    file['user_id'] = user_id

                btn = types.InlineKeyboardButton(text='Back ↩️', callback_data='admin_back_list')
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=response, reply_markup=inline_markup_admin_get_all_numbers('All numbers').add(btn))
                await FSMAdmin.numbers_or_back.set()


@dispatcher.callback_query_handler(state=FSMAdmin.numbers_or_back)
async def admin_back(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'admin_back_list':
        await get_list_users(call)
        await FSMAdmin.choose_user.set()
    elif call.data == 'admin_user_list_numbers':
        await get_user_list_numbers(call, state)
        await FSMAdmin.choose_phone.set()


async def get_user_list_numbers(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as file:
        user_id = file['user_id']
    numbers = db.get_added_numbers_by_owner_id(user_id, 'added')
    btn = types.InlineKeyboardButton(text='Back ↩️', callback_data='admin_back_list')
    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'UserID: <a><b>{user_id}</b></a>\nList numbers quantity: {len(numbers)}', reply_markup=inline_markup_numbers(numbers, db).add(btn), parse_mode='HTML')


@dispatcher.callback_query_handler(state=FSMAdmin.choose_phone)
async def admin_back(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'admin_back_list':
        await get_list_users(call)
        await FSMAdmin.choose_user.set()
    else:
        async with state.proxy() as file:
            user_id = file['user_id']
        for i in db.get_added_numbers_by_owner_id(user_id, 'added'):
            if str(i[0]) == call.data:
                response = f'number: <b>{call.data}</b>' + '\n'
                response += f'api_id: <b>{db.get_api_id(call.data)}</b>' + '\n'
                response += f'api_hash: <b>{db.get_api_hash(call.data)}</b>' + '\n'
                response += f'owner_id: <b>{db.get_owner_id(call.data)}</b>' + '\n'
                response += f'name: <b>{db.get_name(call.data)}</b>' + '\n'
                response += f'send messages quantity: <b>{db.get_message_count(call.data)}</b>'

                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=response, reply_markup=inline_markup_admin_back('Back', 'admin_back_list'), parse_mode='HTML')
                await FSMAdmin.phone_info_back.set()


@dispatcher.callback_query_handler(state=FSMAdmin.phone_info_back)
async def admin_back(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'admin_back_list':
        await get_user_list_numbers(call, state)
        await FSMAdmin.choose_phone.set()


@dispatcher.message_handler(Text(equals='cancel', ignore_case=True), state=FSMAdmin.user)
async def cancel_input_user_id(message: types.Message, state: FSMContext):
    await clear_state(state)
    await bot.send_message(message.chat.id, 'OKS', reply_markup=types.ReplyKeyboardRemove())
    await bot.send_message(message.chat.id, text='<i>What we gonna do machineglytkelly👨‍💻</i>?', reply_markup=inline_markup_admin(), parse_mode='HTML')
    await FSMAdmin.admin_opportunities.set()


@dispatcher.message_handler(content_types=['text'], state=FSMAdmin.user)
async def get_user_id(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, 'Ok', reply_markup=types.ReplyKeyboardRemove())
    if users_db.user_exists(message.text):
        async with state.proxy() as file:
            access = file['access']
            file['user_id'] = message.text
        if access == 'give':
            if users_db.get_access(message.text) == 'start':
                await bot.send_message(message.chat.id, 'For how many days?', reply_markup=reply_markup_call_off('Cancel'))
                await FSMAdmin.days.set()
            else:
                await bot.send_message(message.chat.id, 'This user has already access to bot', reply_markup=inline_markup_admin_back('Back', 'admin_back'))
                await FSMAdmin.cancel.set()
        elif access == 'take_back':
            users_db.set_access(message.text, 'start')
            users_db.set_seconds(message.text, None)
            users_db.set_time(message.text, None)
            users_db.set_period(message.text, None)
            await bot.send_message(message.chat.id, f'Access for user with ChatID <a><b>{message.text}</b></a> was restricted', reply_markup=inline_markup_admin_back('Back', 'admin_back'), parse_mode='HTML')
            await FSMAdmin.cancel.set()
    else:
        await bot.send_message(message.chat.id, 'There is no such user', reply_markup=inline_markup_admin_back('Back', 'admin_back'))
        await FSMAdmin.cancel.set()


@dispatcher.message_handler(content_types=['text'], state=FSMAdmin.days)
async def get_days(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, 'Ok', reply_markup=types.ReplyKeyboardRemove())
    if float(message.text) > 0:
        async with state.proxy() as file:
            user_id = file['user_id']
        users_db.set_access(user_id, 'using')
        seconds = int(time.time())
        users_db.set_seconds(user_id, seconds)
        users_db.set_time(user_id, time.ctime(seconds))
        users_db.set_period(user_id, message.text)
        users_db.increment_purchases(user_id)
        async with state.proxy() as file:
            user_id = file['user_id']
        await bot.send_message(message.chat.id, f'Access for user with ChatID <a><b>{user_id}</b></a> was received', reply_markup=inline_markup_admin_back('Back', 'admin_back'), parse_mode='HTML')
        await FSMAdmin.cancel.set()
    else:
        await bot.send_message(message.chat.id, 'Incorrect ⛔️, try one more time')
        await bot.send_message(message.chat.id, 'For how many days?')
        await FSMAdmin.days.set()


try:
    asyncio.run(executor.start_polling(dispatcher=dispatcher, skip_updates=False))
except Exception as error:
    print(error)
