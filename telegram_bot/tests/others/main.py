import sqlite3
import time
import telebot
import datetime
import random
from telebot import types
from db import Database
#from db import db

bot = telebot.TeleBot('5312729248:AAFPvhJ4LgoFFvtQwPQpqkiV56zZpq1Hu6s')
db = Database('myDB.db')

def input_nickname(message):
    if message.content_type == 'text':
        db.set_nickname(message.text, message.from_user.id)
        bot.send_message(message.chat.id,"спасибо, ваши данные записаны")
    else:
        bot.send_message(message.chat.id,"неправильно")

@bot.message_handler(commands=['start'])
def start(message):
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
        db.set_sub_time(message.date, message.from_user.id)

    if db.no_nickname(message.from_user.id):
        bot.send_message(message.chat.id,"Введите ваше имя")
        bot.register_next_step_handler(message, input_nickname)


    #bot.send_message(message.chat.id, "name: " + str(message.from_user.username) + "\n" + "id: " + str(message.from_user.id))
    #bot.send_message(message.chat.id, "date: " + str(datetime.datetime.utcfromtimestamp(message.date+3600*3)))
    #bot.send_message(message.chat.id, str(message.chat.type))
    s = "Введите любую команду из этого списка\n"
    s += "/geiness \n"
    s += "/cock_size \n"
    s += "/blowjob_chance \n"
    s += "/breaking_news \n"
    s += "/sucking \n"
    s += "/talk \n"

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2, one_time_keyboard=True)
    btn1 = types.KeyboardButton(text="Button1")
    btn2 = types.KeyboardButton(text="Button2")
    kb.add(btn1,btn2)

    bot.send_message(message.chat.id,s)
    bot.send_poll(message.chat.id,question="WILL YOU SUCK MY BALLS",options=['YES','NO','OF COURSE'],correct_option_id=0,timeout=5)

def share(message):
    users_list = db.get_users()
    print(users_list)
    if message.content_type == 'photo':
        for i in users_list:
            try:
                raw = message.photo[2].file_id
                name = raw+".jpg"
                file_info = bot.get_file(raw)
                downloaded_file = bot.download_file(file_info.file_path)
                with open(name,'wb') as new_file:
                    new_file.write(downloaded_file)
                img = open(name, 'rb')
                bot.send_photo(i[0], img)
            except Exception as e:
                pass
    elif message.content_type == 'text':
        for i in users_list:
            try:
                bot.send_message(i[0],message.text)
            except Exception as e:
                pass

@bot.message_handler(commands=['share'])
def start(message):
    print(message.from_user.id)
    if message.chat.id == 628860511:
        bot.send_message(message.chat.id,"Введите сообщение для рассылки")
        bot.register_next_step_handler(message,share)


@bot.message_handler(commands=['geiness'])
def start(message):
    procent = random.randint(0,100)
    bot.send_message(message.chat.id,f"вы гей на {procent}%")

def cool(message):
    if message.content_type == 'photo':
        bot.send_message(message.chat.id,'Nice cock!')
    else:
        bot.send_message(message.chat.id,f"нахуй ты скинул мне что-то формата '{message.content_type}'\n я же сука просил фото дикпика")

@bot.message_handler(commands=['talk'])
def start(message):
    bot.send_message(message.chat.id,"Скинь фото дикпика пж")
    bot.register_next_step_handler(message,cool)

@bot.message_handler(commands=['cock_size'])
def start(message):
    cm = random.randint(1,30)
    bot.send_message(message.chat.id,f"ваш пенис - {cm}см")

@bot.message_handler(commands=['blowjob_chance'])
def start(message):
    procent = random.randint(0,100)
    bot.send_message(message.chat.id,f"шанс того, что вам сегодня оформят отсосик -  {procent}%")

@bot.message_handler(commands=['breaking_news'])
def start(message):
    with open("img/roman.jpg", "rb") as f:
        bot.send_photo(message.chat.id,f,"<a href=\"https://rt.pornhub.com/view_video.php?viewkey=ph625f109f54e37\">КСЕНИЯ КУКАН ПРОСТО В ШОКЕ ОТ ТАКИХ РАЗМЕРОВ !!!</a>", parse_mode='HTMl')

@bot.message_handler(commands=['sucking'])
def start(message):
    kb = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text="ОТСОС В ОБЩАГЕ 🍌️", url="https://rt.pornhub.com/view_video.php?viewkey=ph625f109f54e37")
    btn2 = types.InlineKeyboardButton(text="ОТСОС В УНИВЕРЕ 🏘 ", url="https://rt.pornhub.com/view_video.php?viewkey=ph625f109f54e37")
    btn3 = types.InlineKeyboardButton(text="ОТСОС ЗА БАЛЛЫ 🍌  ➡  💯", url="https://rt.pornhub.com/view_video.php?viewkey=ph625f109f54e37")
    btn4 = types.InlineKeyboardButton(text="ОТСОС ЗА СИГАРЕТУ 🍌  ➡  🚬", url="https://rt.pornhub.com/view_video.php?viewkey=ph625f109f54e37")
    btn5 = types.InlineKeyboardButton(text="ОТСОС ЗА СОЧНИК 🍌  ➡  🥠", url="https://rt.pornhub.com/view_video.php?viewkey=ph625f109f54e37")
    btn6 = types.InlineKeyboardButton(text="ОБРАТНЫЙ ОТСОС 🤔🤔🤔", url="https://rt.pornhub.com/view_video.php?viewkey=ph625f109f54e37")

    kb.add(btn1,btn2,btn3,btn4,btn5,btn6)
    bot.send_message(message.chat.id,"СЛИВ <tg-spoiler><b><i>КСЕНИИ КУКАН</i></b></tg-spoiler>",reply_markup=kb, parse_mode='HTML')


@bot.message_handler(regexp=r"паша [\w+]")
def start(message):
    bot.delete_message(message.chat.id,message.message_id)

@bot.message_handler(regexp=r"катюха [\w+]")
def start(message):
    bot_message = bot.send_message(message.chat.id,message.text)
    time.sleep(5)
    bot.edit_message_text(chat_id=message.chat.id,message_id=bot_message.message_id,text="катюха <b>ЕБАНУЛАСЬ</b>", parse_mode="HTML")

@bot.message_handler(regexp=r"рома [\w+]")
def start(message):
    bot.reply_to(message,"и это верно!")

@bot.message_handler(regexp=r"\+375[ (]{0,2}[\d]{2}[) ]{0,2}[\d-]{7,9}")
def start(message):
    bot.reply_to(message, 'ЭТО НОМЕР ШАБОЛДЫ')


@bot.message_handler(content_types = ['photo'])
def start(message):
    bot.send_message(message.chat.id,message)
    bot.send_message(message.chat.id, 'нахуй ты мне скинул фотку олень')

@bot.message_handler(content_types = ['video'])
def start(message):
    bot.send_message(message.chat.id, 'засунь себе в очко свой видос')

@bot.message_handler(content_types = ['sticker'])
def start(message):
    print(str(message.chat.id))
    bot.send_message(message.chat.id, 'пососи, а не стикер свой кидай хуила ебаная')

@bot.message_handler(func = lambda message: message.text == "катюха")
def start(message):
    bot.send_message(message.chat.id, 'ЕБАНУТАЯ')

@bot.edited_message_handler(func = lambda message: True)
def start(message):
    bot.send_message(message.chat.id, 'нахуй ты редактировал сообщение шалава')


@bot.message_handler(func = lambda message: message.text == "machineglytkelly")
def start(message):
    with open("../../../../python/bot/first_bot/file.txt", "w") as f:
        f.write(message.text)
    with open("../../../../python/bot/first_bot/file.txt", "r") as doc:
        bot.send_document(message.chat.id,doc)

try:
    bot.polling(none_stop=True)
except:
    pass
