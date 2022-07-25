import time
import types

from aiogram import Bot
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

from data_base.db import AccountsDB
from data_base.db_users import UsersDB
from data_base.wbDB import WebScraperDB
from data_base.machineDB import MachineDB
from data_base.errors_db import ErrorsDB

from main_script import Script
from asyncio_browser import WebScraper


class FSMWebScraper(StatesGroup):
    ListNumbers = State()
    opportunities = State()
    last_chance = State()
    number = State()
    password = State()
    choice = State()
    chat = State()
    minutes = State()
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
    sharing_start = State()
    sharing_using = State()
    statistics = State()
    del_list = State()
    condition = State()

    choose_user_WS = State()
    WS_numbers_or_back = State()
    WS_back = State()


class FSMSubAdmin(StatesGroup):
    sub_admin_opps = State()
    input_user = State()
    sub_days = State()
    sub_cancel = State()
    sharing = State()


db = AccountsDB('data_base/accounts.db')
users_db = UsersDB('data_base/accounts.db')
web_scraper_db = WebScraperDB('data_base/accounts.db')
machine_db = MachineDB('data_base/accounts.db')
errors_db = ErrorsDB('data_base/accounts.db')

storage = MemoryStorage()

bot = Bot(token='5583638970:AAE4WgvD77v0eMv1wBEdVkSPCFlSxQUse9U')
#                5440048392:AAEnoo5T26t99sg7Hq8Hh3ojPcc5-Irzc6k     Message Spreader Bot
#                5496675572:AAFpX4KOHcMBHhFwXQqimnGUxf5kQ8G5RYc     SharkBet Bot
dispatcher = Dispatcher(bot=bot, storage=storage)

GlobalList = []
GlobalMachineList = []


ADMIN_LINK = '@denis_mscw'
#            '@shark_bet_admin'

ADIMIN_IDS = [628860511, 899951880]

SUB_ADMIN_IDS = []
#               5256029946


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
            text = f'<i>Вы не имеет доступ к боту ⛔️\nДля получения доступа напишите админу</i> <b>{ADMIN_LINK}</b> 👨‍💻'
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_back('Назад'), parse_mode='HTML')

    elif call.data == 'added_accounts':
        if users_db.get_access(call.message.chat.id) == 'using':
            await get_list_numbers(call)
            await FSMWebScraper.ListNumbers.set()
        else:
            text = f'<i>Вы не имеет доступ к боту ⛔️\nДля получения доступа напишите админу</i> <b>{ADMIN_LINK}</b> 👨‍💻'
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
        global GlobalList
        web_scraper_db.delete_user(message.chat.id)
        for i in GlobalList:
            if int(i['data'][1]) == message.chat.id:
                try:
                    web_scraper: WebScraper
                    web_scraper = i['data'][0]
                    await web_scraper.close()
                except Exception as e:
                    print(e)
                GlobalList.remove(i)
    await clear_state(state)
    await bot.send_message(message.chat.id, '<i>Действие отменено</i> ↩', reply_markup=types.ReplyKeyboardRemove(), parse_mode='HTML')
    await send_menu(message)


@dispatcher.message_handler(Text(equals='назад', ignore_case=True), state=[FSMWebScraper.chat, FSMWebScraper.mailing_text, FSMWebScraper.minutes])
async def cancel_handler(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, '<i>Действие отменено</i> ↩', reply_markup=types.ReplyKeyboardRemove(), parse_mode='HTML')
    async with state.proxy() as file:
        phone = file['phone']
    await bot.send_message(chat_id=message.chat.id, text=f'<i>Аккаунт с номером</i> <code>{phone}</code>📱', reply_markup=inline_markup_opportunities(), parse_mode='HTML')
    await FSMWebScraper.opportunities.set()


@dispatcher.message_handler(Text(equals='cancel', ignore_case=True), state=[FSMAdmin.user, FSMAdmin.sharing, FSMAdmin.del_param, FSMAdmin.sharing_start, FSMAdmin.sharing_using])
async def cancel_input_user_id(message: types.Message, state: FSMContext):
    await clear_state(state)
    await bot.send_message(message.chat.id, 'OKS', reply_markup=types.ReplyKeyboardRemove())
    await bot.send_message(message.chat.id, text='<i>What we gonna do machineglytkelly👨‍💻</i>?', reply_markup=inline_markup_admin(), parse_mode='HTML')
    await FSMAdmin.admin_opportunities.set()


@dispatcher.message_handler(Text(equals='Back', ignore_case=True), state=[FSMSubAdmin.input_user, FSMSubAdmin.sub_days, FSMSubAdmin.sharing])
async def cancel_input_user_id(message: types.Message, state: FSMContext):
    await clear_state(state)
    await bot.send_message(message.chat.id, 'OKS', reply_markup=types.ReplyKeyboardRemove())
    await bot.send_message(message.chat.id, text='<i>What we gonna do sub admin 🦈</i>?', reply_markup=inline_markup_sub_admin(), parse_mode='HTML')
    await FSMSubAdmin.sub_admin_opps.set()


@dispatcher.callback_query_handler(state=FSMAdmin.cancel)
async def admin_back(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'admin_back':
        await clear_state(state)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='<i>What we gonna do machineglytkelly👨‍💻</i>?', reply_markup=inline_markup_admin(), parse_mode='HTML')
        await FSMAdmin.admin_opportunities.set()


@dispatcher.callback_query_handler(state=FSMSubAdmin.sub_cancel)
async def admin_back(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'admin_back':
        await clear_state(state)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='<i>What we gonna do sub admin 🦈</i>?', reply_markup=inline_markup_sub_admin(), parse_mode='HTML')
        await FSMSubAdmin.sub_admin_opps.set()


async def my_profile(call: types.CallbackQuery):
    text = f'💬Ваш ChatID: <b><code>{call.message.chat.id}</code></b>' + '\n'
    login = 'none ⛔️'
    if call.from_user.username is not None:
        login = '@' + call.from_user.username
    text += f'👤Ваш логин: {login}' + '\n'
    response = users_db.get_access(call.message.chat.id)
    access = f'<i>🙅‍♂️Вы не имеете доступа к боту, чтобы получить доступ, напишите админу</i> <b>{ADMIN_LINK}</b> 👨‍💻'
    if response == 'using':
        seconds = users_db.get_seconds(call.message.chat.id)
        period = users_db.get_period(call.message.chat.id) * 24 * 3600
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
            text = '🔹Отправьте ссылку на чат 🔗' + '\n\n'
            text += '⚠<b>Примечание:</b> Бот не может пропарсить <i>Invite ссылку</i> (ссылка, начинающаяся со знака + после https://t.me/)'
            await bot.send_message(call.message.chat.id, text=text, reply_markup=reply_markup_call_off('Назад'), parse_mode='HTML')
            await FSMWebScraper.chat.set()
        else:
            await clear_state(state)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Бот уже запущен на этом аккаунте, выберите другой', reply_markup=inline_markup_back('Главное меню'))
    elif call.data == 'delete_account':
        text = '<i>Вы точно уверены что хотите удалить данный аккаунт с вашего списка?\nПосле удаления данные аккаунта сохранятся и вы сможете опять его добавить</i>'
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
        await FSMWebScraper.ListNumbers.set()
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
        name = get_name(message)
        users_db.set_name(message.chat.id, name)
        users_db.set_access(message.chat.id, 'start')
        text = f'<i>User</i> <b>{name}</b> <i>started using bot</i> 🤖'
        for i in ADIMIN_IDS:
            try:
                await bot.send_message(i, text, parse_mode='HTML')
            except Exception as e:
                print(e)

    await send_menu(message)


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


@dispatcher.message_handler(commands=['menu'])
async def start_menu(message: types.Message, state: FSMContext):
    global GlobalList, GlobalMachineList
    if web_scraper_db.user_exists(message.chat.id):
        web_scraper_db.delete_user(message.chat.id)
        for i in GlobalList:
            if int(i['data'][1]) == message.chat.id:
                try:
                    web_scraper: WebScraper
                    web_scraper = i['data'][0]
                    await web_scraper.close()
                except Exception as e:
                    print(e)
                GlobalList.remove(i)
    if machine_db.user_exists(message.chat.id):
        for i in GlobalMachineList:
            if int(i['data'][1]) == message.chat.id:
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
    wait = await bot.send_message(message.chat.id, '<i>Ожидайте ⏳</i>', parse_mode='HTML', reply_markup=types.ReplyKeyboardRemove())
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
            try:
                scraper = WebScraper()
                await scraper.initialize()

                params = await scraper.input_phone_number(phone)
                if params[0]:
                    web_dict = {'data': [scraper, message.chat.id]}

                    web_scraper_db.add_user(message.chat.id)
                    web_scraper_db.set_web_scraper_id(message.chat.id, str(scraper))

                    global GlobalList
                    GlobalList.append(web_dict)

                    await bot.delete_message(message.chat.id, wait.message_id)
                    await bot.send_message(message.chat.id, '🔹Введи код, отправленный вам в Telegram 🔤', reply_markup=reply_markup_call_off('Отмена'))
                    await FSMWebScraper.password.set()
                else:
                    await bot.delete_message(message.chat.id, wait.message_id)
                    if params[1] == 'alarm':
                        await scraper.remove_number_error()
                        await bot.send_message(message.chat.id, '⛔<b>Введенный вами номер некорректен, повторите процедуру еще раз</b>', parse_mode='HTML')
                        await bot.send_message(message.chat.id, '🔹Введи номер аккаунта Telegram ☎\nНомер формата <b>+7YYYXXXXXXX</b>, или формата любой другой страны\n<b>🔺Примечание:</b> знак ➕ должен обязательно находиться вначале номера', reply_markup=reply_markup_call_off('Отмена'), parse_mode='HTML')
                        await FSMWebScraper.number.set()
                    else:
                        await scraper.close()
                        await clear_state(state)
                        await bot.send_message(message.chat.id, f'⛔<b>Ошибка</b>: {params[1]}\n<i>Попробуйте позже</i>', reply_markup=inline_markup_back('На главное меню'), parse_mode='HTML')
            except Exception as e:
                await bot.delete_message(message.chat.id, wait.message_id)
                await clear_state(state)
                await bot.send_message(message.chat.id, f'<b>Ошибка:</b> {e}', reply_markup=inline_markup_back('Главное меню'), parse_mode='HTML')

    else:
        await bot.delete_message(message.chat.id, wait.message_id)
        await bot.send_message(message.chat.id, '⛔<b>Введенный вами номер некорректен (знак ➕ должен обязательно находиться вначале номера), повторите процедуру еще раз</b>', parse_mode='HTML')
        await bot.send_message(message.chat.id, '🔹Введи номер аккаунта Telegram ☎\nНомер формата <b>+7YYYXXXXXXX</b>, или формата любой другой страны\n<b>🔺Примечание:</b> знак ➕ должен обязательно находиться вначале номера', reply_markup=reply_markup_call_off('Отмена'), parse_mode='HTML')
        await FSMWebScraper.number.set()


# GET PASSWORD WHEN REGISTER NEW ACCOUNT # WEB_SCRAPER

@dispatcher.message_handler(content_types=['text'], state=FSMWebScraper.password)
async def get_password(message: types.Message, state: FSMContext):
    wait = await bot.send_message(message.chat.id, '<i>Ожидайте ⏳</i>', parse_mode='HTML', reply_markup=types.ReplyKeyboardRemove())

    global GlobalList
    actual_browser: WebScraper

    count = 0

    for i in GlobalList:
        if int(i['data'][1]) == message.chat.id:
            count += 1
            actual_browser = i['data'][0]
            try:
                params = await actual_browser.input_password(password=message.text, owner_id=message.chat.id, errors_db=errors_db)
                if not params[0]:
                    if params[1] == 'alarm':
                        await actual_browser.remove_password_error()
                        await bot.delete_message(message.chat.id, wait.message_id)
                        await bot.send_message(message.chat.id, '⛔<b>Неверный код, попробуйте ввести код еще раз либо добавьте данный аккаунт позже</b>', reply_markup=reply_markup_call_off('Отмена'), parse_mode='HTML')
                        await FSMWebScraper.password.set()
                    else:
                        web_scraper_db.delete_user(message.chat.id)
                        GlobalList.remove(i)
                        await bot.delete_message(message.chat.id, wait.message_id)
                        await clear_state(state)
                        await bot.send_message(message.chat.id, '<b>Технические неполадки</b> 🛠... <i>Попробуйте позже или добавьте другой аккаунт</i>',  reply_markup=inline_markup_back('На главное меню'), parse_mode='HTML')
                else:
                    api = await actual_browser.get_api(errors_db)
                    web_scraper_db.delete_user(message.chat.id)
                    GlobalList.remove(i)
                    if not api[3]:
                        await bot.delete_message(message.chat.id, wait.message_id)
                        await clear_state(state)
                        await bot.send_message(message.chat.id, '<b>Технические неполадки</b> 🛠... <i>Попробуйте позже или добавьте другой аккаунт</i>',  reply_markup=inline_markup_back('На главное меню'), parse_mode='HTML')
                    else:
                        phone = api[2]
                        db.add_phone_number(phone)
                        db.set_api_id(phone, api[0])
                        db.set_api_hash(phone, api[1])
                        db.set_owner_id(phone, message.chat.id)

                        await bot.delete_message(message.chat.id, wait.message_id)
                        await bot.send_message(message.chat.id, '<i>Аккаунт успешно добавлен</i> 🧩', reply_markup=inline_markup_choice(), parse_mode='HTML')
                        await FSMWebScraper.choice.set()
            except Exception as error:
                try:
                    web_scraper_db.delete_user(message.chat.id)
                    GlobalList.remove(i)
                except Exception as e:
                    print(e)
                await bot.delete_message(message.chat.id, wait.message_id)
                await clear_state(state)
                await bot.send_message(message.chat.id, f'<b>Ошибка:</b> {str(error)}', reply_markup=inline_markup_back('Главное меню'), parse_mode='HTML')

    if count == 0:
        await bot.delete_message(message.chat.id, wait.message_id)
        await clear_state(state)
        await bot.send_message(message.chat.id, '<i>Технические неполадки, попробуйте позже</i> 🛠', reply_markup=inline_markup_back('Главное меню'), parse_mode='HTML')


# SUB MENU WHEN ADDING SUCCESS NEW NUMBER


@dispatcher.callback_query_handler(state=FSMWebScraper.choice)
async def get_choice(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'start_mailing':
        async with state.proxy() as file:
            phone = file['phone']
        if db.get_condition(phone) == 0:
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            text = '🔹Отправьте ссылку на чат 🔗' + '\n\n'
            text += '⚠<b>Примечание:</b> Бот не может пропарсить <i>Invite ссылку</i> (ссылка, начинающаяся со знака + после https://t.me/)'
            await bot.send_message(call.message.chat.id, text=text, reply_markup=reply_markup_call_off('Назад'), parse_mode='HTML')
            await FSMWebScraper.chat.set()
        else:
            await clear_state(state)
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='🚫<b>Бот уже запущен на этом аккаунте, выберите другой</b>', reply_markup=inline_markup_back('Главное меню'), parse_mode='HTML')

    elif call.data == 'add_account':
        await clear_state(state)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        await bot.send_message(call.message.chat.id, '🔹Введи номер аккаунта Telegram ☎\nНомер формата <b>+7YYYXXXXXXX</b>, или формата любой другой страны\n<b>🔺Примечание:</b> знак ➕ должен обязательно находиться вначале номера', reply_markup=reply_markup_call_off('Отмена'), parse_mode='HTML')
        await FSMWebScraper.number.set()
    elif call.data == 'main_menu':
        await clear_state(state)
        await edit_to_menu(call.message)


# GET CHAT FOR PARSING

@dispatcher.message_handler(content_types=['text'], state=FSMWebScraper.chat)
async def get_chat(message: types.Message, state: FSMContext):
    async with state.proxy() as file:
        file['chat'] = message.text
    await bot.send_message(message.chat.id, '<i>Принято</i> ✅', reply_markup=types.ReplyKeyboardRemove(), parse_mode='HTML')
    text = '🔹Укажите максимальное время последней активности пользователей, которым будет писать бот (в минутах)⌚' + '\n\n'
    text += '<i>Целое число от 5 до 1440</i>' + '\n\n'
    await bot.send_message(message.chat.id, text=text, reply_markup=reply_markup_call_off('Назад'), parse_mode='HTML')
    await FSMWebScraper.minutes.set()


# GET MINUTES

@dispatcher.message_handler(content_types=['text'], state=FSMWebScraper.minutes)
async def get_minutes(message: types.Message, state: FSMContext):
    try:
        minutes = int(message.text)
        if minutes >= 5 and minutes <= 1440:
            async with state.proxy() as file:
                file['minutes'] = message.text
            await bot.send_message(message.chat.id, '<i>Принято</i> ✅', reply_markup=types.ReplyKeyboardRemove(), parse_mode='HTML')
            await bot.send_message(message.chat.id, '🔹Отправьте сообщение для рассылки 📩', reply_markup=reply_markup_call_off('Назад'))
            await FSMWebScraper.mailing_text.set()
        else:
            await bot.send_message(message.chat.id, '⛔Некорректный ввод: введите целое число минут от 5 до 1440')
            await FSMWebScraper.minutes.set()
    except Exception as e:
        await bot.send_message(message.chat.id, '⛔Некорректный ввод: введите целое число минут от 5 до 1440')
        await FSMWebScraper.minutes.set()


# GET TEXT TO MAILING

@dispatcher.message_handler(content_types=['text'], state=FSMWebScraper.mailing_text)
async def get_mailing_text(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, '<i>Принято</i> ✅', reply_markup=types.ReplyKeyboardRemove(), parse_mode='HTML')
    async with state.proxy() as file:
        try:
            file['mailing_text'] = message.text
            phone = file['phone']
            session_name = ''.join(random.choice(string.digits) for _ in range(random.randrange(8, 12)))
            machine = Script(session_name=session_name,
                             api_id=db.get_api_id(phone),
                             api_hash=db.get_api_hash(phone),
                             phone_number=phone,
                             chat_link=file['chat'],
                             data=message.text,
                             minutes=int(file['minutes']))
            db.set_mailing_message(phone, message.text)
            await bot.send_message(message.chat.id, '<i>Отправляем код в Telegram</i> ⏳', parse_mode='HTML')
            params = await machine.verify()
            if params[0]:
                dict_machine = {'data': [machine, message.chat.id]}

                machine_db.add_user(message.chat.id)
                machine_db.set_machine_id(message.chat.id, str(machine))

                global GlobalMachineList
                GlobalMachineList.append(dict_machine)

                await bot.send_message(message.chat.id, '🔹Введите код, отправленный вам в Telegram 🔢\n❗<b>Примечание:</b> перед вводом кода убедитесь, что на аккаунте выключена двухэтапная аутентификация', reply_markup=reply_markup_call_off('Не приходит код, вернуться на главное меню'), parse_mode='HTML')
                await FSMWebScraper.telegram_code.set()
            else:
                await clear_state(state)
                await bot.send_message(message.chat.id, '⛔<b>Ошибка:</b> ' + str(params[1]), reply_markup=inline_markup_back('На главное меню'), parse_mode='HTML')
        except Exception as e:
            print(e)
            await clear_state(state)
            await bot.send_message(message.chat.id, '⛔<b>Ошибка:</b> ' + str(e), reply_markup=inline_markup_back('На главное меню'), parse_mode='HTML')


# TELEGRAM_CODE FINAL PART

@dispatcher.message_handler(content_types=['text'], state=FSMWebScraper.telegram_code)
async def get_telegram_code(message: types.Message, state: FSMContext):
    global GlobalMachineList
    if message.text == 'Не приходит код, вернуться на главное меню':
        await bot.send_message(message.chat.id, '<i>Принято</i> ✅', reply_markup=types.ReplyKeyboardRemove(), parse_mode='HTML')
        await clear_state(state)
        if machine_db.user_exists(message.chat.id):
            machine_db.delete_user(message.chat.id)
            for i in GlobalMachineList:
                if int(i['data'][1]) == message.chat.id:
                    GlobalMachineList.remove(i)
        await send_menu(message)
    else:
        text = '<i>Ожидайте</i> ⏳' + '\n\n'
        text += '<i>Время ожидания зависит от количества участников чата, так как бот полностью перебирает всех пользователей чата и выбирает каждый раз рандомных 🎲</i>'
        wait = await bot.send_message(message.chat.id, text=text, reply_markup=types.ReplyKeyboardRemove(), parse_mode='HTML')

        actual_machine: Script

        count = 0

        for i in GlobalMachineList:
            if int(i['data'][1]) == message.chat.id:
                count += 1
                actual_machine = i['data'][0]
                GlobalMachineList.remove(i)
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
                            await bot.delete_message(chat_id=message.chat.id, message_id=wait.message_id)
                            await clear_state(state)
                            await bot.send_message(message.chat.id, '⛔<b>Ошибка:</b> ' + str(chat_params[1]), reply_markup=inline_markup_back('На главное меню'), parse_mode='HTML')

                    else:
                        await bot.delete_message(chat_id=message.chat.id, message_id=wait.message_id)
                        await clear_state(state)
                        await bot.send_message(message.chat.id, '⛔<b>Ошибка:</b> ' + str(params[1]), reply_markup=inline_markup_back('На главное меню'), parse_mode='HTML')
                except Exception as error:
                    await bot.delete_message(chat_id=message.chat.id, message_id=wait.message_id)
                    await clear_state(state)
                    await bot.send_message(message.chat.id, '⛔<b>Ошибка:</b> ' + str(error), reply_markup=inline_markup_back('На главное меню'), parse_mode='HTML')

        if count == 0:
            await clear_state(state)
            await bot.send_message(message.chat.id, '<i>Технические неполадки, попробуйте позже</i> 🛠', reply_markup=inline_markup_back('Главное меню'), parse_mode='HTML')


# MODERATOR PART


@dispatcher.message_handler(commands=['moderator'], state=['*'])
async def start_moderator(message: types.Message, state: FSMContext):
    await clear_state(state)
    for i in ADIMIN_IDS:
        if message.chat.id == i:
            await bot.send_message(message.chat.id, text='<i>What we gonna do machineglytkelly👨‍💻</i>?', reply_markup=inline_markup_admin(), parse_mode='HTML')
            await FSMAdmin.admin_opportunities.set()
    for i in SUB_ADMIN_IDS:
        if message.chat.id == i:
            await bot.send_message(message.chat.id, text='<i>What we gonna do sub admin 🦈</i>?', reply_markup=inline_markup_sub_admin(), parse_mode='HTML')
            await FSMSubAdmin.sub_admin_opps.set()


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
        await get_all_names(call)
        await FSMAdmin.cancel.set()
    elif call.data == 'del_list':
        text = f'WebScraper: {len(GlobalList)}\nMachineGun: {len(GlobalMachineList)}'
        btn = types.InlineKeyboardButton(text='Back', callback_data='admin_back')
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_del_list_keyboard().add(btn))
        await FSMAdmin.del_list.set()
    elif call.data == 'access_users':
        await get_list_using_users(call)
        await FSMAdmin.choose_user.set()
    elif call.data == 'web_scraper':
        await get_list_using_users(call)
        await FSMAdmin.choose_user_WS.set()
    elif call.data == 'main_menu':
        await clear_state(state)
        await edit_to_menu(call.message)
    elif call.data == 'del_func':
        await bot.send_message(call.message.chat.id, 'Input del_params', reply_markup=reply_markup_call_off('Cancel'))
        await FSMAdmin.del_param.set()
    elif call.data == 'period_list':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=str(users_db.get_periods_by('using')), reply_markup=inline_markup_admin_back('Back', 'admin_back'))
        await FSMAdmin.cancel.set()
    elif call.data == 'chats':
        await get_all_chats(call)
        await FSMAdmin.cancel.set()
    elif call.data == 'sharing':
        await bot.send_message(call.message.chat.id, 'Input data for sharing', reply_markup=reply_markup_call_off('Cancel'))
        await FSMAdmin.sharing.set()
    elif call.data == 'sharing_start':
        await bot.send_message(call.message.chat.id, 'Input data for sharing with start 😫', reply_markup=reply_markup_call_off('Cancel'))
        await FSMAdmin.sharing_start.set()
    elif call.data == 'sharing_using':
        await bot.send_message(call.message.chat.id, 'Input data for sharing with using 🤑', reply_markup=reply_markup_call_off('Cancel'))
        await FSMAdmin.sharing_using.set()
    elif call.data == 'statistics':
        await clear_state(state)
        await get_statistics(call)
        await FSMAdmin.statistics.set()
    elif call.data == 'conditions':
        text = '<i>Choose what condition all accounts are gonna have</i>'
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_condition(), parse_mode='HTML')
        await FSMAdmin.condition.set()


@dispatcher.callback_query_handler(state=FSMAdmin.condition)
async def set_condition(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'back':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='<i>What we gonna do machineglytkelly👨‍💻</i>?', reply_markup=inline_markup_admin(), parse_mode='HTML')
        await FSMAdmin.admin_opportunities.set()
    elif call.data == 'true':
        db.set_same_condition(True)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='<i>What we gonna do machineglytkelly👨‍💻</i>?', reply_markup=inline_markup_admin(), parse_mode='HTML')
        await FSMAdmin.admin_opportunities.set()
    elif call.data == 'false':
        db.set_same_condition(False)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='<i>What we gonna do machineglytkelly👨‍💻</i>?', reply_markup=inline_markup_admin(), parse_mode='HTML')
        await FSMAdmin.admin_opportunities.set()


async def get_all_names(call: types.CallbackQuery):
    name_list = users_db.get_all_names()
    text = f'Users quantity: <b>{len(name_list)}</b>' + '\n'
    for i in name_list:
        if i[0] is not None:
            text += i[0] + '\n'
    if len(text) > 4096:
        for x in range(0, len(text), 4096):
            await bot.send_message(call.message.chat.id, text[x:x+4096])
    else:
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, parse_mode='HTML')
    await bot.send_message(call.message.chat.id, '<b>List if all users</b>', reply_markup=inline_markup_admin_back('Back', 'admin_back'), parse_mode='HTML')


async def get_all_chats(call: types.CallbackQuery):
    chats = db.get_all_chats()
    text = f'Chats quantity: <b>{len(chats)}</b>' + '\n'
    for i in chats:
        if i[0] is not None:
            text += i[0] + '\n'
    if len(text) > 4096:
        for x in range(0, len(text), 4096):
            await bot.send_message(call.message.chat.id, text[x:x+4096])
    else:
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, parse_mode='HTML')
    await bot.send_message(call.message.chat.id, '<b>List of all chats</b>', reply_markup=inline_markup_admin_back('Back', 'admin_back'), parse_mode='HTML')


@dispatcher.callback_query_handler(state=FSMAdmin.del_list)
async def del_list(call: types.CallbackQuery):
    if call.data == 'web_scraper':
        GlobalList.clear()
    elif call.data == 'machine_gun':
        GlobalMachineList.clear()

    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='<i>What we gonna do machineglytkelly👨‍💻</i>?', reply_markup=inline_markup_admin(), parse_mode='HTML')
    await FSMAdmin.admin_opportunities.set()


@dispatcher.message_handler(state=FSMAdmin.del_param)
async def del_access(message: types.Message):
    users_by_period = users_db.get_users_by_period(message.text)
    await bot.send_message(message.chat.id, 'Ok', reply_markup=types.ReplyKeyboardRemove())
    text = 'Access was restricted on accounts with ChatID: \n'
    for i in users_by_period:
        print((users_db.get_seconds(i[0]) + users_db.get_period(i[0])*24*3600) - time.time())
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


@dispatcher.message_handler(content_types=['text'], state=FSMAdmin.sharing_start)
async def start_sharing(message: types.Message, state: FSMContext):
    for i in users_db.get_users_by_access('start'):
        try:
            await bot.send_message(i[0], message.text, reply_markup=inline_markup_get_bot())
        except Exception as error:
            print(error)
    await bot.send_message(message.chat.id, 'Done', reply_markup=types.ReplyKeyboardRemove())
    await start_moderator(message, state)


@dispatcher.message_handler(content_types=['text'], state=FSMAdmin.sharing_using)
async def start_sharing(message: types.Message, state: FSMContext):
    for i in users_db.get_users_by_access('using'):
        try:
            await bot.send_message(i[0], message.text, reply_markup=inline_markup_ok())
        except Exception as error:
            print(error)
    await bot.send_message(message.chat.id, 'Done', reply_markup=types.ReplyKeyboardRemove())
    await start_moderator(message, state)


async def get_statistics(call):
    text = f'Users quantity: <b>{len(users_db.get_users())}</b>' + '\n'
    text += f'Active clients: <b>{len(users_db.get_users_by_access("using"))}</b>' + '\n'
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


@dispatcher.callback_query_handler(state=FSMAdmin.choose_user_WS)
async def start(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'admin_back':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='<i>What we gonna do machineglytkelly👨‍💻</i>?', reply_markup=inline_markup_admin(), parse_mode='HTML')
        await clear_state(state)
        await FSMAdmin.admin_opportunities.set()
    else:
        for i in users_db.get_users_by_access('using'):
            if str(i[0]) == call.data:

                async with state.proxy() as file:
                    file['user_id'] = str(i[0])

                text = '<i>All numbers of user:</i>'
                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_numbers_web_scraper(phone=str(call.data), errors_db=errors_db), parse_mode='HTML')
                await FSMAdmin.WS_numbers_or_back.set()


@dispatcher.callback_query_handler(state=FSMAdmin.WS_numbers_or_back)
async def start(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'admin_back':
        await get_list_using_users(call)
        await FSMAdmin.choose_user_WS.set()
    else:
        async with state.proxy() as file:
            user_id = file['user_id']

        for i in errors_db.get_numbers_by_owner_id(user_id):
            if call.data == str(i[0]):

                text = 'Information about number for <b>WS</b>' + '\n\n'
                text += f'error_status: <i>{errors_db.get_error_status(i[0])}</i>'

                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_admin_back('Back', 'admin_back'), parse_mode='HTML')
                await FSMAdmin.WS_back.set()


@dispatcher.callback_query_handler(state=FSMAdmin.WS_back)
async def start(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'admin_back':
        async with state.proxy() as file:
            user_id = file['user_id']
        text = 'All numbers of user'
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text, reply_markup=inline_markup_numbers_web_scraper(phone=str(user_id), errors_db=errors_db))
        await FSMAdmin.WS_numbers_or_back.set()


@dispatcher.callback_query_handler(state=FSMAdmin.choose_user)
async def start(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'admin_back':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='<i>What we gonna do machineglytkelly👨‍💻</i>?', reply_markup=inline_markup_admin(), parse_mode='HTML')
        await clear_state(state)
        await FSMAdmin.admin_opportunities.set()
    else:
        for i in users_db.get_users_by_access('using'):
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
        await get_list_using_users(call)
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
        await get_list_using_users(call)
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
                response += f'send messages quantity: <b>{db.get_message_count(call.data)}</b>' + '\n'
                response += f'mailing_text: <b>{db.get_mailing_message(call.data)}</b>' + '\n'
                response += f'chat_link: <b>{db.get_chat(call.data)}</b>'

                await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=response, reply_markup=inline_markup_admin_back('Back', 'admin_back_list'), parse_mode='HTML')
                await FSMAdmin.phone_info_back.set()


@dispatcher.callback_query_handler(state=FSMAdmin.phone_info_back)
async def admin_back(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'admin_back_list':
        await get_user_list_numbers(call, state)
        await FSMAdmin.choose_phone.set()


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
            if users_db.get_access(message.text) == 'using':
                users_db.set_access(message.text, 'start')
                users_db.set_seconds(message.text, None)
                users_db.set_time(message.text, None)
                users_db.set_period(message.text, None)
                await bot.send_message(message.chat.id, f'Access for user with ChatID <a><b>{message.text}</b></a> was restricted', reply_markup=inline_markup_admin_back('Back', 'admin_back'), parse_mode='HTML')
                await FSMAdmin.cancel.set()
            else:
                await bot.send_message(message.chat.id, 'This user does not have access', reply_markup=inline_markup_admin_back('Back', 'admin_back'), parse_mode='HTML')
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


# SUB ADMIN OPPORTUNITIES

@dispatcher.callback_query_handler(state=FSMSubAdmin.sub_admin_opps)
async def start_admin_opportunities(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'give_access':
        await bot.send_message(call.message.chat.id, 'Send me user ID', reply_markup=reply_markup_call_off('Back'))
        async with state.proxy() as file:
            file['access'] = 'give'
        await FSMSubAdmin.input_user.set()
    elif call.data == 'take_back_access':
        await bot.send_message(call.message.chat.id, 'Send me user ID', reply_markup=reply_markup_call_off('Back'))
        async with state.proxy() as file:
            file['access'] = 'take_back'
        await FSMSubAdmin.input_user.set()
    elif call.data == 'sharing':
        text = 'Send me text to send to all users of bot 🦈'
        await bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=reply_markup_call_off('Back'))
        await FSMSubAdmin.sharing.set()
    elif call.data == 'main_menu':
        await clear_state(state)
        await edit_to_menu(call.message)


@dispatcher.message_handler(content_types=['text'], state=FSMSubAdmin.input_user)
async def get_user_id(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, 'Ok', reply_markup=types.ReplyKeyboardRemove())
    if users_db.user_exists(message.text):
        async with state.proxy() as file:
            access = file['access']
            file['user_id'] = message.text
        if access == 'give':
            if users_db.get_access(message.text) == 'start':
                await bot.send_message(message.chat.id, 'For how many days?', reply_markup=reply_markup_call_off('Cancel'))
                await FSMSubAdmin.sub_days.set()
            else:
                await bot.send_message(message.chat.id, 'This user has already access to bot', reply_markup=inline_markup_admin_back('Back', 'admin_back'))
                await FSMSubAdmin.sub_cancel.set()
        elif access == 'take_back':
            if users_db.get_access(message.text) == 'using':
                users_db.set_access(message.text, 'start')
                users_db.set_seconds(message.text, None)
                users_db.set_time(message.text, None)
                users_db.set_period(message.text, None)
                await bot.send_message(message.chat.id, f'Access for user with ChatID <a><b>{message.text}</b></a> was restricted', reply_markup=inline_markup_admin_back('Back', 'admin_back'), parse_mode='HTML')
                await FSMSubAdmin.sub_cancel.set()
            else:
                await bot.send_message(message.chat.id, 'This user does not have access', reply_markup=inline_markup_admin_back('Back', 'admin_back'))
                await FSMSubAdmin.sub_cancel.set()
    else:
        await bot.send_message(message.chat.id, 'There is no such user', reply_markup=inline_markup_admin_back('Back', 'admin_back'))
        await FSMSubAdmin.sub_cancel.set()


@dispatcher.message_handler(content_types=['text'], state=FSMSubAdmin.sub_days)
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
        await FSMSubAdmin.sub_cancel.set()
    else:
        await bot.send_message(message.chat.id, 'Incorrect ⛔️, try one more time')
        await bot.send_message(message.chat.id, 'For how many days?')
        await FSMSubAdmin.sub_days.set()


@dispatcher.message_handler(content_types=['text'], state=FSMSubAdmin.sharing)
async def send_to_users(message: types.Message, state: FSMContext):
    for i in users_db.get_users():
        try:
            await bot.send_message(chat_id=int(i[0]), text=message.text, reply_markup=inline_markup_ok())
        except Exception as e:
            print(e)

    await bot.send_message(message.chat.id, 'Done ', reply_markup=types.ReplyKeyboardRemove())
    await bot.send_message(message.chat.id, text='<i>What we gonna do sub admin 🦈</i>?', reply_markup=inline_markup_sub_admin(), parse_mode='HTML')
    await FSMSubAdmin.sub_admin_opps.set()


try:
    asyncio.run(executor.start_polling(dispatcher=dispatcher, skip_updates=False))
except Exception as error:
    print(error)
