from aiogram import types
from data_base.db import AccountsDB
from data_base.errors_db import ErrorsDB


ADMIN_LINK = 'https://t.me/denis_mscw'
#            'https://t.me/shark_bet_admin'


def inline_markup_menu():
    kb = types.InlineKeyboardMarkup(row_width=2)

    btn1 = types.InlineKeyboardButton('Добавить аккаунт', callback_data='add_account')
    btn2 = types.InlineKeyboardButton('Добавленные аккаунты', callback_data='added_accounts')
    btn3 = types.InlineKeyboardButton('Купить аккаунты Telegram 📲', url='https://5sim.net/')
    btn4 = types.InlineKeyboardButton('📤 ПОЛНОЕ ОПИСАНИЕ БОТА 🤖', url='https://telegra.ph/Telegram-BOT-dlya-rassylki-soobshchenij-v-LS-09-14')
    btn5 = types.InlineKeyboardButton('Админ 👨‍💻', url=ADMIN_LINK)
    btn6 = types.InlineKeyboardButton('Мой профиль 💰', callback_data='profile')

    kb.add(btn1, btn2)
    kb.row(btn3)
    kb.row(btn4)
    kb.row(btn5, btn6)

    return kb


def inline_markup_back(text):
    kb = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text + ' ↩️', callback_data='back')

    kb.add(btn1)

    return kb


def inline_markup_ok():
    kb = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton('OK ✅', callback_data='ok',)

    kb.add(btn1)

    return kb


def inline_markup_get_bot():
    kb = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton('ПОЛУЧИТЬ БОТА 🤖', url='https://t.me/denis_mscw')

    kb.add(btn1)

    return kb


def inline_markup_admin_back(text, callback):
    kb = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text + '↩️', callback_data=callback)

    kb.add(btn1)

    return kb


def inline_markup_admin_get_all_numbers(text):
    kb = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text=text, callback_data='admin_user_list_numbers')

    kb.add(btn1)

    return kb


def inline_markup_add():
    kb = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton('Добавать еще аккаунт', callback_data='one_more_account')

    kb.add(btn1)

    return kb


def reply_markup_call_off(text):
    kb = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton(text=text)

    kb.add(btn1)

    return kb


def inline_markup_numbers(numbers: list, db: AccountsDB):
    kb = types.InlineKeyboardMarkup(row_width=1)
    if len(numbers) > 98:
        while len(numbers) > 98:
            numbers.pop(0)
    for i in numbers:
        text = i[0] + ' '
        name = db.get_name(i[0])
        if name is not None:
            text += name
        btn = types.InlineKeyboardButton(text=str(text), callback_data=str(i[0]))
        kb.add(btn)

    return kb


def inline_markup_numbers_web_scraper(phone, errors_db: ErrorsDB):
    kb = types.InlineKeyboardMarkup(row_width=1)
    numbers = errors_db.get_numbers_by_owner_id(phone)
    if len(numbers) > 98:
        while len(numbers) > 98:
            numbers.pop(0)
    for i in numbers:
        btn = types.InlineKeyboardButton(text=str(i[0]), callback_data=str(i[0]))
        kb.add(btn)

    btn = types.InlineKeyboardButton('Back↩️', callback_data='admin_back')

    kb.add(btn)

    return kb


def inline_markup_choice():
    kb = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton('Начать рассылку ✅', callback_data='start_mailing')
    btn2 = types.InlineKeyboardButton('Добавить аккаунт ➕', callback_data='add_account')
    btn3 = types.InlineKeyboardButton('Главное меню 📱', callback_data='main_menu')

    kb.add(btn1, btn2, btn3)

    return kb


def inline_markup_opportunities():
    kb = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton('Начать рассылку ✅', callback_data='start_mailing')
    btn2 = types.InlineKeyboardButton('Убрать аккаунт ❌', callback_data='delete_account')
    btn3 = types.InlineKeyboardButton('Назад ↩️', callback_data='back_opportunities')

    kb.add(btn1, btn2, btn3)

    return kb


def inline_markup_yes_no():
    kb = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton('Да, убрать ❌', callback_data='yes')
    btn2 = types.InlineKeyboardButton('Нет, оставить 😉', callback_data='no')

    kb.add(btn1, btn2)

    return kb


def inline_markup_is_premium():
    kb = types.InlineKeyboardMarkup(row_width=2)

    btn1 = types.InlineKeyboardButton('Да', callback_data='yes')
    btn2 = types.InlineKeyboardButton('Нет', callback_data='no')
    btn3 = types.InlineKeyboardButton('Назад ↩️', callback_data='back')

    kb.add(btn1, btn2, btn3)

    return kb


def inline_markup_admin():
    kb = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton('Give access ✅', callback_data='give_access')
    btn2 = types.InlineKeyboardButton('Take back access ❌', callback_data='take_back_access')
    btn3 = types.InlineKeyboardButton('All users', callback_data='all_users')
    btn4 = types.InlineKeyboardButton('Delete List', callback_data='del_list')
    btn5 = types.InlineKeyboardButton('All users with access', callback_data='access_users')
    btn6 = types.InlineKeyboardButton('Fucking WebScraper', callback_data='web_scraper')
    btn7 = types.InlineKeyboardButton('Delete Function', callback_data='del_func')
    btn8 = types.InlineKeyboardButton('Period List', callback_data='period_list')
    btn9 = types.InlineKeyboardButton('Chats', callback_data='chats')
    btn10 = types.InlineKeyboardButton('Statistics 📊', callback_data='statistics')
    btn11 = types.InlineKeyboardButton('Conditions', callback_data='conditions')
    btn12 = types.InlineKeyboardButton('Sharing', callback_data='sharing')
    btn13 = types.InlineKeyboardButton('Sharing with start 😫', callback_data='sharing_start')
    btn14 = types.InlineKeyboardButton('Sharing with using 🤑', callback_data='sharing_using')
    btn15 = types.InlineKeyboardButton('Manual adding accounts', callback_data='manual_adding')
    btn16 = types.InlineKeyboardButton('Main menu', callback_data='main_menu')

    kb.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11, btn12, btn13, btn14, btn15, btn16)

    return kb


def inline_markup_sub_admin():
    kb = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton('Give access ✅', callback_data='give_access')
    btn2 = types.InlineKeyboardButton('Take back access ❌', callback_data='take_back_access')
    btn3 = types.InlineKeyboardButton('Sharing', callback_data='sharing')
    btn4 = types.InlineKeyboardButton('Main menu', callback_data='main_menu')

    kb.add(btn1, btn2, btn3, btn4)

    return kb


def inline_del_list_keyboard():
    kb = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton('WebScraper', callback_data='web_scraper')
    btn2 = types.InlineKeyboardButton('MachineGun', callback_data='machine_gun')

    kb.add(btn1, btn2)

    return kb


def inline_markup_users(users: list):
    kb = types.InlineKeyboardMarkup(row_width=1)
    for i in users:
        btn = types.InlineKeyboardButton(text=str(i[0] + ' ' + i[1]), callback_data=str(i[0]))
        kb.add(btn)

    return kb


def inline_markup_condition():
    kb = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton('True', callback_data='true')
    btn2 = types.InlineKeyboardButton('False', callback_data='false')
    btn3 = types.InlineKeyboardButton('Back ↩', callback_data='back')

    kb.add(btn1, btn2, btn3)

    return kb

