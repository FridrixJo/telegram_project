from aiogram import types


def inline_markup_menu():
    kb = types.InlineKeyboardMarkup(row_width=2)

    btn1 = types.InlineKeyboardButton('Добвить аккаунт', callback_data='add_account')
    btn2 = types.InlineKeyboardButton('Добавленные аккаунты', callback_data='added_accounts')
    btn3 = types.InlineKeyboardButton('Админ', url='https://t.me/denis_mscw')
    btn4 = types.InlineKeyboardButton('О боте', callback_data='about')
    btn5 = types.InlineKeyboardButton('Купить аккаунты Telegram', url='https://5sim.net/')

    kb.add(btn1, btn2, btn3, btn4)
    kb.row(btn5)

    return kb


def inline_markup_back(text):
    kb = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text, callback_data='back')

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


def reply_markup_choice():
    kb = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)

    btn1 = types.KeyboardButton('Добавить аккаунт')
    btn2 = types.KeyboardButton('Главное меню')
    btn3 = types.KeyboardButton('Начать рассылку')

    kb.add(btn1, btn2, btn3)

    return kb
