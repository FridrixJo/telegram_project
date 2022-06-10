#!/usr/bin/python
# -*- coding: utf8 -*-

import telebot
from telebot import types
from data_bases.users import UsersDB

import time
import datetime
import random
import re

from data_bases.db import AccountsDB
from data_bases.users import UsersDB

from scripts.get_authorized import Api_Data

bot = telebot.TeleBot('5583638970:AAE9RTGf3u3hzbvV9VkhwJfQSRXfQfuwRxw')

db = AccountsDB('../data_bases/accounts.db')
users_db = UsersDB('../data_bases/accounts.db')


def inline_markup_menu():
    kb = types.InlineKeyboardMarkup(row_width=2)

    btn1 = types.InlineKeyboardButton('Добвить аккаунт', callback_data='add_account')
    btn2 = types.InlineKeyboardButton('Активные аккаунты', callback_data='active_accounts')
    btn3 = types.InlineKeyboardButton('Админ', url='https://t.me/denis_mscw')
    btn4 = types.InlineKeyboardButton('О боте', callback_data='about')
    btn5 = types.InlineKeyboardButton('Купить аккаунты Telegram', url='https://5sim.net/')

    kb.add(btn1,btn2,btn3,btn4)
    kb.row(btn5)

    return kb

def inline_markup_back():
    kb = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton('Назад', callback_data='back')

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


def menu(message):
    bot.send_message(message.chat.id, 'Главное меню', reply_markup=inline_markup_menu())


@bot.callback_query_handler(func=lambda call: True)
def start(call):
    if call.data == 'back':
        bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='Главное меню', reply_markup=inline_markup_menu())

    if call.data == 'add_account':
        bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        add_account(call.message, 'Добавление акканута, введите номер в формате 79161234567')

    if call.data == 'active_accounts':
       bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='Список всех активных аккаунтов', reply_markup=inline_markup_back())

    if call.data == 'about':
        bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        about(call.message)

def input_number(message, prev_message_id):
    reg = r"[\d]{9,16}"
    if re.search(reg,message.text):
        bot.edit_message_text(chat_id=message.chat.id, message_id=prev_message_id, text='Немного подождите ...')
        if db.account_exists(message.text):
            pass
        else:
            data = Api_Data()
            params_list = data.login(message.text)

            phone = message.text

            if len(params_list) >= 3:
                db.add_phone_number(phone)
                db.set_api_id(phone, params_list[0])
                db.set_api_hash(phone, params_list[1])

        bot.delete_message(chat_id=message.chat.id, message_id=prev_message_id)

        time.sleep(0.2)

        sent = bot.send_message(message.chat.id, 'Введите код, отправленный вам в Telegram', reply_markup=reply_markup_call_off('Не приходит код, добавить другой акканут'))
        message_id = sent.message_id
        bot.register_next_step_handler(sent, input_code_combination, message_id)
    elif message.text == 'Отмена':
        menu(message)
    else:
        add_account(message, 'Номер введен некорректно\nВведите номер, например 79261234567')

def input_code_combination(message, prev_message_id):
    if message.text == 'Не приходит код, добавить другой акканут':
        add_account(message, 'Добавление акканута, введите номер в формате 79161234567')
    else:
        time.sleep(0.2)
        bot.delete_message(chat_id=message.chat.id, message_id=prev_message_id)
        time.sleep(0.2)

        sent = bot.send_message(message.chat.id, 'Аккаунт добавлен')
        time.sleep(1)
        bot.delete_message(chat_id=message.chat.id, message_id=sent.message_id)

        add_account(message, 'Добавьте еще аккаунты, введите номер в формате 79161234567')


def add_account(message, text):
    sent = bot.send_message(message.chat.id, text=text, reply_markup=reply_markup_call_off('Отмена'))
    message_id = sent.message_id
    bot.register_next_step_handler(sent, input_number, message_id)


def about(message):
    sent = bot.send_message(message.chat.id, 'Информация о боте', reply_markup=inline_markup_back())


@bot.message_handler(commands=['menu'])
def start(message):
    menu(message)

@bot.message_handler(commands=['start'])
def start(message):
    print(message)
    print("\n\n\n")
    menu(message)


try:
    bot.polling(none_stop=True)
except Exception as e:
    print(e)

