#!/usr/bin/python
# -*- coding: utf8 -*-
import asyncio

import telebot
from telebot import types
from data_bases.db_users import UsersDB

import time
import datetime
import random
import re

from data_bases.db import AccountsDB
from data_bases.db_users import UsersDB

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
    btn2 = types.InlineKeyboardButton('Добавленные аккаунты', callback_data='added_accounts')
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


def inline_markup_numbers(list: list):
    kb = types.InlineKeyboardMarkup(row_width=1)
    for i in list:
        btn = types.InlineKeyboardButton(text=str(i[0]), callback_data=str(i[0]))
        kb.add(btn)

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

    if call.data == 'added_accounts':
        list = db.get_numbers_by_owner_id(call.message.chat.id)
        btn = types.InlineKeyboardButton('Назад', callback_data='back')
        bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='Список всех активных аккаунтов', reply_markup=inline_markup_numbers(list).add(btn))

    if call.data == 'about':
        bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        about(call.message)

    list = db.get_numbers_by_owner_id(call.message.chat.id)
    for i in list:
        if call.data == str(i[0]):
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            give_choice(call.message, 'Выберите одно из трех предложенных', call.data)



def send_password(message, text, data):
    sent = bot.send_message(message.chat.id, text, reply_markup=reply_markup_call_off('Не приходит код, добавить другой акканут'))
    message_id = sent.message_id
    bot.register_next_step_handler(sent, input_code_combination, message_id, data)


def input_code_combination(message, prev_message_id, data):
    if message.content_type == 'text':
        if message.text == 'Не приходит код, добавить другой акканут':
            add_account(message, 'Добавление акканута, введите номер в формате +79161234567')
        else:
            response = data.input_password(message.text)
            bot.delete_message(chat_id=message.chat.id, message_id=prev_message_id)

            if not response[0]:
                text = ''
                if response[1] == 'invalid password':
                    text = 'Неверный код, попробуйте добавить другой аккаунт.\nВведите номер в формате +79161234567'
                    add_account(message, text)
                else:
                    sent = bot.send_message(message.chat.id, 'Возникли некоторые проблемы, попробуйте позже')
                    time.sleep(5)
                    bot.delete_message(chat_id=message.chat.id, message_id=sent.message_id)
                    menu(message)
            else:
                waiting_message = bot.send_message(message.chat.id, 'Немного подождите ...')

                params = data.getting_data()
                bot.delete_message(chat_id=message.chat.id, message_id=waiting_message.message_id)

                if params[3] is True:
                    Phone = params[2]
                    db.add_phone_number(Phone)
                    db.set_api_id(Phone, params[0])
                    db.set_api_hash(Phone, params[1])
                    db.set_owner(Phone, message.from_user.id)

                    time.sleep(0.2)

                    give_choice(message, text='Аккаунт добавлен, что делаем дальше?', phone_number=Phone)
                else:
                    bot.send_message(message.chat.id, str(params[4]), reply_markup=inline_markup_back('Вернуться на главное меню'))
    else:
        bot.delete_message(chat_id=message.id, message_id=prev_message_id)
        send_password(message, 'Код введен некорректно (отправьте код, высланный вам в Telegram, в виде текста)', data)


def input_number(message, prev_message_id):
    bot.delete_message(chat_id=message.chat.id, message_id=prev_message_id)
    if message.content_type == 'text':
        if message.text == 'Отмена':
            menu(message)
        else:
            if db.account_exists(message.text):
                give_choice(message, 'Выберите одно из трёх предложенных', phone_number=message.text)
            else:
                waiting_message = bot.send_message(message.chat.id, 'Немного подождите ...')

                Phone = message.text

                data = Api_Data(Phone)

                response = data.login()

                bot.delete_message(chat_id=message.chat.id, message_id=waiting_message.message_id)

                if response[0] is False:
                    text = ''
                    if response[1] == 'invalid number':
                        text = 'Несущесвующий или неверный номер, отправьте номер аккаунта Telegram ещё раз (формат: +79261234567)'
                        add_account(message, text)
                    else:
                        bot.send_message(message.chat.id, str(response[1]), reply_markup=inline_markup_back('Вернуться на главное меню'))
                else:
                    send_password(message, 'Введите код, отправленный вам в Telegram', data)
    else:
        add_account(message, 'Номер введен некорректно, отправьте номер аккаунта Telegram в виде текста (формат: +79261234567)')



def add_account(message, text):
    print(message.chat.id)
    sent = bot.send_message(message.chat.id, text=text, reply_markup=reply_markup_call_off('Отмена'))
    bot.register_next_step_handler(sent, input_number, sent.message_id)


def about(message):
    sent = bot.send_message(message.chat.id, 'Информация о боте', reply_markup=inline_markup_back('Назад'))


def input_chat_link(message, prev_message_id, phone_number):
    bot.delete_message(chat_id=message.chat.id, message_id=prev_message_id)
    if message.content_type == 'text':
        if message.text == 'Отмена':
            give_choice(message, text='Выберите одно из трёх предложенных', phone_number=phone_number)
        else:
            chat_link = message.text

            get_mailing_text(message, phone_number, chat_link)
    else:
        get_chat_link(message, text='Ссылка на чат введена некорректно, отправьте корректную ссылку в виде текста', phone_number=phone_number)


def get_chat_link(message, text, phone_number):
    sent = bot.send_message(message.chat.id, text=text, reply_markup=reply_markup_call_off('Отмена'))
    message_id = sent.message_id
    bot.register_next_step_handler(sent, input_chat_link, message_id, phone_number)


def give_choice(message, text, phone_number):
    btn1 = types.KeyboardButton(text='Начать рассылку')
    btn2 = types.KeyboardButton(text='Добавить аккаунт')
    sent = bot.send_message(message.chat.id, text, reply_markup=reply_markup_call_off('Главное меню').add(btn1, btn2))
    bot.register_next_step_handler(sent, get_continue, sent.message_id, phone_number)


def get_continue(message, prev_message_id, phone_number):
    bot.delete_message(chat_id=message.chat.id, message_id=prev_message_id)
    if message.content_type == 'text':
        if message.text == 'Начать рассылку':
            get_chat_link(message, 'Ссылка на чат: ', phone_number=phone_number)
        elif message.text == 'Добавить аккаунт':
            add_account(message, text='Добавление акканута, введите номер в формате +79161234567')
        elif message.text == 'Главное меню':
            menu(message)
        else:
            give_choice(message, text='Выберите одно из трёх предложенных', phone_number=phone_number)
    else:
        give_choice(message, text='Выберите одно из трёх предложенных', phone_number=phone_number)


def get_mailing_text(message, phone_number, chat_link):
    sent = bot.send_message(message.chat.id, 'Введите текст для рассылки')
    bot.register_next_step_handler(sent, mailing_text, sent.message_id, phone_number, chat_link)


def mailing_text(message, prev_message_id, phone_number, chat_link):
    if message.content_type == 'text':
        if message.text == 'Отмена':
            bot.delete_message(chat_id=message.chat.id, message_id=prev_message_id)
            give_choice(message, text='Выберите одно из трёх предложенных', phone_number=phone_number)
        else:
            try:
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
            send_telegram_code(message,text='Получаем сессию вашего аккаунта в Telegram.\n' + 'Введите отправленный вам код', machine=machine)
    else:
        bot.delete_message(chat_id=message.chat.id, message_id=prev_message_id)
        give_choice(message, text='Выберите одно из трёх предложенных', phone_number=phone_number)


def send_telegram_code(message, text, machine):
    response = machine.verify()
    if response[0]:
        btn = types.KeyboardButton(text='Отправить код еще раз')
        sent = bot.send_message(message.chat.id, text, reply_markup=reply_markup_call_off('Не приходит код, добавить другой акканут').add(btn))
        bot.register_next_step_handler(sent, get_code, sent.message_id, machine)
    else:
        sent = bot.send_message(message.chat.id, 'Ошибка: ' + str(response[1]), reply_markup=inline_markup_back('Вернуться на главное меню'))


def sent_telegram_code_twice(message, text, machine):
    btn = types.KeyboardButton(text='Отправить код еще раз')
    sent = bot.send_message(message.chat.id, text, reply_markup=reply_markup_call_off('Не приходит код, добавить другой акканут').add(btn))
    bot.register_next_step_handler(sent, get_code, sent.message_id, machine)


def resend_telegram_code(message, text, machine):
    response = machine.resend_code()
    if response[0]:
        btn = types.KeyboardButton(text='Отправить код еще раз')
        sent = bot.send_message(message.chat.id, text, reply_markup=reply_markup_call_off('Не приходит код, добавить другой акканут').add(btn))
        bot.register_next_step_handler(sent, get_code, sent.message_id, machine)
    else:
        sent = bot.send_message(message.chat.id, 'Ошибка: ' + str(response[1]), reply_markup=inline_markup_back('Вернуться на главное меню'))



def get_code(message, prev_message_id, machine: Script):
    bot.delete_message(chat_id=message.chat.id, message_id=prev_message_id)
    if message.content_type == 'text':
        if message.text == 'Не приходит код, добавить другой акканут':
            add_account(message, 'Добавление акканута, введите номер в формате +79161234567')
        elif message.text == 'Отправить код еще раз':
            resend_telegram_code(message, 'Введите код, отправленный вам повторно в Telegram', machine)
        else:
            list = machine.input_code(message.text)
            time.sleep(2)

            if list[0] is True:
                bot.send_message(message.chat.id, 'Бот запущен', reply_markup=inline_markup_back('Главное меню'))
                x = threading.Thread(target=machine.start, daemon=True)
                x.start()
                print(x)
                #x.start()
            else:
                sent = bot.send_message(message.chat.id, 'Ошибка: ' + str(list[1]), reply_markup=inline_markup_back('Вернуться на главное меню'))
    else:
        sent_telegram_code_twice(message, text='Некорректный ввод, введите код, отправленный вам в Telegram, в виде текста', machine=machine)


@bot.message_handler(commands=['menu'])
def start(message):
    menu(message)

@bot.message_handler(commands=['start'])
def start(message: types.Message):
    menu(message)


try:
    bot.polling(none_stop=True)
except Exception as e:
    print(e)

