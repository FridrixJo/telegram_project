#!/usr/bin/python
# -*- coding: utf8 -*-

import time
import telebot
import datetime
import random
from telebot import types
from AppleDB import AppleDB, AppleCategoryDB
from parse import Parse
from key_generator import Password
import threading

import glob

bot = telebot.TeleBot('5382870818:AAG8crCq66ThT3UeYDlrKrpt3MhQRbRtf-0')
db = AppleDB("apple_db.db")
ct = AppleCategoryDB("apple_db.db")
url = 'https://www.kufar.by/l/mobilnye-telefony/mt~apple?sort=lst.d'
pr = Parse(url)
Key = False
Pass = Password()


def get_search_area(message):
    # section city

    db.set_parse_status(message.from_user.id, "False")

    kb = types.ReplyKeyboardMarkup(row_width=2,one_time_keyboard=True,resize_keyboard=True)
    btn1 = types.KeyboardButton("Минск")
    btn2 = types.KeyboardButton("Гомель")
    btn3 = types.KeyboardButton("Брест")
    btn4 = types.KeyboardButton("Гродно")
    btn5 = types.KeyboardButton("Могилев")
    btn6 = types.KeyboardButton("Витебск")
    btn7 = types.KeyboardButton("Вся Беларусь")

    kb.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)

    sent = bot.send_message(message.from_user.id ,"Выберите город",reply_markup=kb)
    bot.register_next_step_handler(sent, set_search_area)


def set_search_area(message):

    if message.text == 'Минск':
        db.set_search_area(message.from_user.id, "/r~minsk")
    elif message.text == 'Гомель':
        db.set_search_area(message.from_user.id, "/r~gomel")
    elif message.text == 'Брест':
        db.set_search_area(message.from_user.id, "/r~brest")
    elif message.text == 'Гродно':
        db.set_search_area(message.from_user.id, "/r~grodno")
    elif message.text == 'Могилев':
        db.set_search_area(message.from_user.id, "/r~mogilev")
    elif message.text == 'Витебск':
        db.set_search_area(message.from_user.id, "/r~vitebsk")
    elif message.text == 'Вся Беларусь':
        db.set_search_area(message.from_user.id, "")
    else:
        db.set_search_area(message.from_user.id, "/r~minsk")

    bot.send_message(message.from_user.id,'Область поиска установлена')

    get_category(message)


def get_category(message):
    kb = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)

    btn1 = types.KeyboardButton("Компьютерная техника")
    btn2 = types.KeyboardButton("Телефоны и планшеты")
    btn3 = types.KeyboardButton("Электроника")
    btn4 = types.KeyboardButton("Бытовая техника")
    btn5 = types.KeyboardButton("Женский гардероб")
    btn6 = types.KeyboardButton("Мужской гардероб")
    btn7 = types.KeyboardButton("Красота и здоровье")
    btn8 = types.KeyboardButton("Мебель")
    btn9 = types.KeyboardButton("Все для дома")
    btn10 = types.KeyboardButton("Ремонт и стройка")
    btn11 = types.KeyboardButton("Прочее ...")

    kb.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11)

    sent = bot.send_message(message.chat.id, "Выберите категорию товара")
    bot.register_next_step_handler(message.from_user.id, set_category)

def create_KeyBoard(message, category):
    kb = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, resize_keyboard=True)

    btn1 = types.KeyboardButton(str(ct.get_cat1(category)))
    btn2 = types.KeyboardButton(str(ct.get_cat2(category)))
    btn3 = types.KeyboardButton(str(ct.get_cat3(category)))
    btn4 = types.KeyboardButton(str(ct.get_cat4(category)))
    btn5 = types.KeyboardButton(str(ct.get_cat5(category)))
    btn6 = types.KeyboardButton(str(ct.get_cat6(category)))

    kb.add(btn1, btn2, btn3, btn4, btn5, btn6)

    sent = bot.send_message(message.chat.id, "Выберите подкатегорию товара")
    bot.register_next_step_handler(message.from_user.id, set_sub_categoty, category)

def set_sub_categoty(message, category):
    if message.text == ct.get_cat1(category):
        db.set_category(message.chat.id, str(ct.get_link_cat1(category)))
    elif message.text == ct.get_cat2(category):
        db.set_category(message.chat.id, str(ct.get_link_cat2(category)))
    elif message.text == ct.get_cat3(category):
        db.set_category(message.chat.id, str(ct.get_link_cat3(category)))
    elif message.text == ct.get_cat4(category):
        db.set_category(message.chat.id, str(ct.get_link_cat4(category)))
    elif message.text == ct.get_cat5(category):
        db.set_category(message.chat.id, str(ct.get_link_cat5(category)))
    elif message.text == ct.get_cat6(category):
        db.set_category(message.chat.id, str(ct.get_link_cat6(category)))


    sent = bot.send_message(message.from_user.id,"Что будете искать\n(например, холодильник)")
    bot.register_next_step_handler(sent, get_request)


def set_category(message):
    if message.text == 'Компьютерная техника':
        create_KeyBoard(message, message.text)
    elif message.text == 'Телефоны и планшеты':
        create_KeyBoard(message, message.text)
    elif message.text == 'Электроника':
        create_KeyBoard(message, message.text)
    elif message.text == 'Бытовая техника':
        create_KeyBoard(message, message.text)
    elif message.text == 'Женский гардероб':
        create_KeyBoard(message, message.text)
    elif message.text == 'Мужской гардероб':
        create_KeyBoard(message, message.text)
    elif message.text == 'Красота и здоровье':
        create_KeyBoard(message, message.text)
    elif message.text == 'Мебель':
        create_KeyBoard(message, message.text)
    elif message.text == 'Все для дома':
        create_KeyBoard(message, message.text)
    elif message.text == 'Ремонт и стройка':
        create_KeyBoard(message, message.text)
    elif message.text == 'Прочее ...':
        create_KeyBoard(message, message.text)
    else:
        create_KeyBoard(message, 'Прочее ...')


def get_request(message):
    # section type
    href = f"https://www.kufar.by/l{db.get_search_area(message.from_user.id)}?ot=1&query={message.text}&rgn=all"
    print(href)
        # https://www.kufar.by/l?ot=1&query=iphone&rgn=all all belarus
        # https://www.kufar.by/l/r~minsk?ot=1&query=iphone&rgn=all minsk
        # https://www.kufar.by/l/r~minsk/mobilnye-telefony?ot=1&query=iphone&rgn=all
        # https://www.kufar.by/l/mobilnye-telefony?ot=1&query=iphone category whole belarus

    db.set_page_url(message.from_user.id, href)

    kb1 = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(text="Перейти к странице", url=href)

    kb1.add(btn)

    bot.send_message(message.chat.id,"Проверьте правильность ссылки, по которой будет осуществяться поиск\n",reply_markup=kb1)

    kb2 = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2, one_time_keyboard=True)
    btn1 = types.KeyboardButton(text="Да✅\nНачать поиск")
    btn2 = types.KeyboardButton(text="Нет, изменить параметры")

    kb2.add(btn1,btn2)
    sent = bot.send_message(message.chat.id,"Все ли верно?",reply_markup= kb2)

    bot.register_next_step_handler(sent, complete_request)

def complete_request(message):
    if message.text == "Да✅\nНачать поиск":
        start_parsing(message)
    elif message.text == "Нет, изменить параметры":
        get_search_area(message)
    else:
        bot.send_message(message.chat.id,"Некорректный ввод, попробуйте еще раз")
        get_search_area(message)


def start_parsing(message):
    db.set_parse_status(message.from_user.id, "True")

    kb = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True, one_time_keyboard=True)

    btn1 = types.KeyboardButton(text="Изменить параметры поиска")
    btn2 = types.KeyboardButton(text="Остановить бота")

    kb.add(btn1, btn2)

    sent = bot.send_message(message.chat.id, "С этого момента вы будете получать объявления со старницы, по которой осуществлялся запрос", reply_markup=kb)
    bot.register_next_step_handler(sent, bot_params)


    x = threading.Thread(target=endless_parsing, args=(message,), daemon=True)
    x.start()


def endless_parsing(message):
    active_post = took_last_post(message, db.get_page_url(message.from_user.id))
    while True:
        last_post_link = took_last_post(message, db.get_page_url(message.from_user.id))
        if db.get_parse_status(message.from_user.id) == "False":
            break
        print(active_post)
        print(last_post_link)
        if active_post != last_post_link:
            active_post = last_post_link
            print_last_post(message, db.get_page_url(message.from_user.id))
        else:
            time.sleep(15)

def bot_params(message):
    if message.text == "Изменить параметры поиска":
        db.set_parse_status(message.from_user.id, "False")
        get_search_area(message)
    elif message.text == "Остановить бота":
        db.set_parse_status(message.from_user.id, "False")

        kb = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True, one_time_keyboard=True)

        btn1 = types.KeyboardButton(text="Изменить параметры поиска")
        btn2 = types.KeyboardButton(text="Запустить бота")

        kb.add(btn1, btn2)

        sent = bot.send_message(message.chat.id, "Бот приостановлен", reply_markup=kb)
        bot.register_next_step_handler(sent, bot_stopped)

def bot_stopped(message):
    if message.text == "Изменить параметры поиска":
        get_search_area(message)
    elif message.text == "Запустить бота":
        start_parsing(message)

def took_last_post(message, search_area):
    l = pr.get_link_in_turple(search_area)
    return l


def print_last_post(message, search_area):

    l = pr.get_turple(message.from_user.id, search_area)
    print(l)

    n = len(glob.glob(f'img/{message.from_user.id}/*'))

    media = []

    for i in range(0,n):
        img = open(f'img/{message.from_user.id}/file'+str(i+1)+'.jpg', 'rb')
        if len(media) >= 8:
            break
        media.append(types.InputMediaPhoto(img))
    # print len(glob.glob('/tmp/*'))
    try:
        bot.send_media_group(message.chat.id,media)
    except Exception as e:
        print(e,"media_group")

    s = "<b>"+l[1]+"</b>\n"+"<b>"+l[2]+"</b>\n"+"<i>"+l[3]+"</i>\n"+"<i>"+l[4]+"</i>\n"

    kb = types.InlineKeyboardMarkup(row_width=1)

    btn = types.InlineKeyboardButton(text="Перейти к объявлению", url=l[0])
    kb.add(btn)

    bot.send_message(message.from_user.id, s, parse_mode="HTML", reply_markup=kb)



@bot.message_handler(commands=['start'])
def start(message):
    db.set_parse_status(message.from_user.id, "False")
    if not db.user_exists(message.from_user.id):
        sent = bot.send_message(message.chat.id, "Введите ключ доступа")
        bot.register_next_step_handler(sent, ask_user)
    else:
        print(4)
        get_search_area(message)

@bot.message_handler(commands=['del'])
def start(message):
    db.delete_all()

def ask_user(message):
    global Key
    if message.text == Pass.get_admin_password() or message.text == Pass.get_trial_password() or message.text == Pass.get_premium_password():
        db.add_user(message.from_user.id)
        db.set_sub_time(message.from_user.id,datetime.datetime.utcfromtimestamp(message.date+3600*3))

        bot.send_message(message.chat.id,"Вы авторизованы")
        Key = True

        if message.text == Pass.get_admin_password():
            db.set_privacy(message.from_user.id, "admin")
            get_search_area(message)

        if message.text == Pass.get_trial_password():
            db.set_privacy(message.from_user.id, "trial")
            get_search_area(message)

        if message.text == Pass.get_premium_password():
            db.set_privacy(message.from_user.id, "premium")
            get_search_area(message)

    else:
        Key = False
        bot.send_message(message.chat.id,"Неверный ключ доступа")

        sent = bot.send_message(message.chat.id, "Попытайтесь еще раз")
        bot.register_next_step_handler(sent, ask_user)

@bot.message_handler(commands=['admin'])
def start(message):
    sent = bot.send_message(message.chat.id, "Введите ключ доступа для админа")
    bot.register_next_step_handler(sent, ask_admin)

def ask_admin(message):
    if message.text == Pass.get_admin_password():
        db.set_privacy(message.from_user.id, message.text)

        admin_working(message)

    else:
        sent = bot.send_message(message.chat.id, "fake-admin попытайся еще раз")
        bot.register_next_step_handler(sent, ask_admin)

def admin_working(message):
    kb = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)

    btn1 = types.KeyboardButton(text="Set TrialPassword")
    btn2 = types.KeyboardButton(text="Set PremiumPassword")
    btn3 = types.KeyboardButton(text="User list")

    kb.add(btn1, btn2, btn3)

    sent = bot.send_message(message.chat.id,"Дорогой machineglytkelly выбери, что хочешь",reply_markup=kb)
    bot.register_next_step_handler(sent, set_passwords)

def set_passwords(message):
    if message.text == "Set TrialPassword":
        Pass.set_trial_password()
        bot.send_message(message.chat.id, str(Pass.get_trial_password()))
    elif message.text == "Set PremiumPassword":
        Pass.set_premium_password()
        bot.send_message(message.chat.id, str(Pass.get_premium_password()))
    elif message.text == "User list":
        id_list = db.get_users()
        sub_time_list = db.get_users_sub_time()
        privacy_list = db.get_users_privacy()

        string_list = "<b>ALL USERS:</b>\n\n"

        for i in range(len(id_list)):
            string_list += "id: " + str(id_list[i][0]) + "\n" + "time: " + str(sub_time_list[i][0]) + "\n" + "privacy: " + str(privacy_list[i][0]) + "\n\n"

        bot.send_message(message.chat.id, string_list,parse_mode="HTML")

    kb = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)

    btn1 = types.KeyboardButton(text="GO GO GO")
    btn2 = types.KeyboardButton(text="Назад")

    kb.add(btn1, btn2)

    sent = bot.send_message(message.chat.id, "Начать работу или вернуться назад?", reply_markup=kb)
    bot.register_next_step_handler(sent, admin_start)

def admin_start(message):
    if message.text == "GO GO GO":
        get_search_area(message)
    elif message.text == "Назад":
        admin_working(message)

try:
    bot.polling(none_stop=True)
except Exception as e:
    print(e)
