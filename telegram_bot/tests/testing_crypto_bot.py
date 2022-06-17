import telebot
from telebot import types

bot = telebot.TeleBot('5529433048:AAFUl1of5wVk3f9kTDWcPBsHfKInz7LPWto')

@bot.message_handler(content_types=['document'])
def start(message):
    bot.send_message(message.chat.id, message)


@bot.message_handler(func=lambda message:True)
def start(message):
    bot.send_message(message.chat.id, message)

try:
    bot.polling(none_stop=True)
except Exception as e:
    print(e)
