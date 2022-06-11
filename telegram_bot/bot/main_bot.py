#!/usr/bin/python
# -*- coding: utf8 -*-
import asyncio

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
from scripts.main_script import Script

from asyncio import set_event_loop, new_event_loop

import threading

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


def menu(message):
    bot.send_message(message.chat.id, 'Главное меню', reply_markup=inline_markup_menu())


@bot.callback_query_handler(func=lambda call: True)
def start(call):
    if call.data == 'back':
        bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='Главное меню', reply_markup=inline_markup_menu())

    if call.data == 'add_account':
        bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        add_account(call.message, 'Добавление акканута, введите номер в формате +79161234567')

    if call.data == 'active_accounts':
       bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='Список всех активных аккаунтов', reply_markup=inline_markup_back('Назад'))

    if call.data == 'about':
        bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        about(call.message)

    if call.data == 'start':
        bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        get_chat_link(call.message)


def input_code_combination(message, prev_message_id, data):
    if message.text == 'Не приходит код, добавить другой акканут':
        add_account(message, 'Добавление акканута, введите номер в формате +79161234567')
    else:
        data.input_password(message.text)
        #print("qwertyjhgfdsdfghjhgfdghjkjhgfdfgh")
        bot.delete_message(chat_id=message.chat.id, message_id=prev_message_id)
        waiting_message = bot.send_message(message.chat.id, 'Немного подождите ...')

        params = data.getting_data()
        if len(params):
            Phone = params[2]
            db.add_phone_number(Phone)
            db.set_api_id(Phone, params[0])
            db.set_api_hash(Phone, params[1])

        time.sleep(0.2)

        bot.delete_message(chat_id=message.chat.id, message_id=waiting_message.message_id)

        bot.send_message(message.chat.id, str(params[0] + "  :  " + str(params[1])))

        btn = types.InlineKeyboardButton(text='Начать рассылку', callback_data='start')
        sent = bot.send_message(message.chat.id, 'Аккаунт добавлен', reply_markup=reply_markup_call_off('Главное меню').add(btn))
        bot.register_next_step_handler(sent, get_chat_link, sent.message_id, params[2])


def input_number(message, prev_message_id):
    print(prev_message_id)
    if message.text == 'Отмена':
        menu(message)
    else:
        bot.delete_message(chat_id=message.chat.id, message_id=prev_message_id)
        if db.account_exists(message.text):
            btn = types.InlineKeyboardButton(text='Начать рассылку', callback_data='start')
            sent = bot.send_message(message.chat.id, 'Аккаунт добавлен', reply_markup=reply_markup_call_off('Главное меню').add(btn))
            bot.register_next_step_handler(sent, get_chat_link, sent.message_id, message.text)

        else:
            waiting_message = bot.send_message(message.chat.id, 'Немного подождите ...')

            Phone = message.text

            data = Api_Data(Phone)

            data.open_browser()
            data.login(Phone)

            bot.delete_message(chat_id=message.chat.id, message_id=waiting_message.message_id)
            sent = bot.send_message(message.chat.id, 'Введите код, отправленный вам в Telegram', reply_markup=reply_markup_call_off('Не приходит код, добавить другой акканут'))
            message_id = sent.message_id
            bot.register_next_step_handler(sent, input_code_combination, message_id, data)



def add_account(message, text):
    sent = bot.send_message(message.chat.id, text=text, reply_markup=reply_markup_call_off('Отмена'))
    message_id = sent.message_id
    print(message_id)
    bot.register_next_step_handler(sent, input_number, message_id)


def about(message):
    sent = bot.send_message(message.chat.id, 'Информация о боте', reply_markup=inline_markup_back('Назад'))


def input_chat_link(message, prev_message_id, phone_number):
    if message.text == 'Отмена':
        menu(message)
    else:
        print(123456789)

        bot.delete_message(chat_id=message.chat.id, message_id=prev_message_id)

        chat_link = message.text

        sent = bot.send_message(message.chat.id, 'Введите текст для рассылки')
        bot.register_next_step_handler(sent, mailing_text, sent.message_id, phone_number, chat_link)


def get_chat_link(message, prev_message_id, phone_number):
    bot.delete_message(message.chat.id, prev_message_id)
    sent = bot.send_message(message.chat.id, text='Ссылка на чат:', reply_markup=reply_markup_call_off('Отмена'))
    message_id = sent.message_id
    bot.register_next_step_handler(sent, input_chat_link, message_id, phone_number)


def mailing_text(message, prev_message_id, phone_number, chat_link):
    if message.text == 'Отмена':
        menu(message)
    else:
        try:
            set_event_loop(asyncio.new_event_loop())
            machine = Script(session_name=str(phone_number),
                             api_id=db.get_api_id(phone_number),
                             api_hash=db.get_api_hash(phone_number),
                             phone_number=phone_number,
                             chat_link=str(chat_link),
                             data=str(message.text))
        except Exception as e:
            print(e)
            return

        bot.delete_message(chat_id=message.chat.id, message_id=prev_message_id)

        if machine.get_session() is False:
            sent = bot.send_message(message.chat.id, 'Получаем сессию ...\n' +
                                          'Введите код, отправленный вам в Telegram', reply_markup=reply_markup_call_off('Не приходит код, добавить другой акканут'))
            machine.verify()
            bot.register_next_step_handler(sent, get_code, sent.message_id, machine)
        else:
            machine.start()
            bot.send_message(message.chat.id, 'Бот запущен', reply_markup=inline_markup_back('Главное меню'))

def get_code(message, prev_message_id, machine):
    if message.text == 'Не приходит код, добавить другой акканут':
        add_account(message, 'Добавление акканута, введите номер в формате +79161234567')
    else:
        if machine.input_code(message.text) is True:
            bot.send_message(message.chat.id, 'Бот запущен', reply_markup=inline_markup_back('Главное меню'))
            machine.start()



@bot.message_handler(commands=['menu'])
def start(message):
    menu(message)

@bot.message_handler(commands=['start'])
def start(message):
    menu(message)


try:
    bot.polling(none_stop=True)
except Exception as e:
    print(e)

