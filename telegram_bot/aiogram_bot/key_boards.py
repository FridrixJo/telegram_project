from aiogram import types


def inline_markup_menu():
    kb = types.InlineKeyboardMarkup(row_width=2)

    btn1 = types.InlineKeyboardButton('Добавить аккаунт', callback_data='add_account')
    btn2 = types.InlineKeyboardButton('Добавленные аккаунты', callback_data='added_accounts')
    btn3 = types.InlineKeyboardButton('Админ 👨‍💻', url='https://t.me/denis_mscw')
    btn4 = types.InlineKeyboardButton('О боте 🤖', callback_data='about')
    btn5 = types.InlineKeyboardButton('Купить аккаунты Telegram 📲', url='https://5sim.net/')
    btn6 = types.InlineKeyboardButton('Мой профиль 💰', callback_data='profile')

    kb.add(btn1, btn2, btn3, btn4)
    kb.row(btn5)
    kb.row(btn6)

    return kb


def inline_markup_back(text):
    kb = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text + '↩️', callback_data='back')

    kb.add(btn1)

    return kb


def inline_markup_admin_back(text):
    kb = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text + '↩️', callback_data='admin_back')

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


def inline_markup_numbers(numbers: list):
    kb = types.InlineKeyboardMarkup(row_width=1)
    for i in numbers:
        btn = types.InlineKeyboardButton(text=str(i[0]), callback_data=str(i[0]))
        kb.add(btn)

    return kb


def inline_markup_choice():
    kb = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton('Добавить аккаунт', callback_data='add_account')
    btn2 = types.InlineKeyboardButton('Главное меню', callback_data='main_menu')
    btn3 = types.InlineKeyboardButton('Начать рассылку', callback_data='start_mailing')

    kb.add(btn3, btn1, btn2)

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


def inline_markup_admin():
    kb = types.InlineKeyboardMarkup(row_width=1)

    btn1 = types.InlineKeyboardButton('Give access ✅', callback_data='give_access')
    btn2 = types.InlineKeyboardButton('Take back access ❌', callback_data='take_back_access')
    btn3 = types.InlineKeyboardButton('All users ', callback_data='all_users')

    kb.add(btn1, btn2, btn3)

    return kb

