#!/usr/bin/python
# -*- coding: utf8 -*-
import string

from pyrogram import Client
from pyrogram import types
from data_base.queue import QueueDB
import random
import asyncio

from config import *

db = QueueDB('data_base/queue.db')

app = Client(name='SESSION', api_id=API_ID, api_hash=API_HASH, phone_number=PHONE_NUMBER)


PHRASES = [
    'приветик, девушка ✌🏻' + '\n' + 'ты безумно красивая 😍',
    'hi, my love ❤️',
    'привет ✌🏻, ты слишком красивая 😘'
]


@app.on_message()
async def get_messages(client, message: types.Message):
    if db.get_work() == 1:
        if message.chat.id == CHAT_ID:
            if message.from_user.id == TARGET_ID and db.get_head() != 1 and message.text != '.':
                db.set_head(head=1)
                db.inc_count()
            elif message.text == db.get_symbol() or (message.text.find(db.get_symbol()) >= 0 and len(message.text) < 20):
                if db.get_count() == db.get_admin_count():
                    db.set_count(count=0)
                    await app.send_message(chat_id=CHAT_ID, text=db.get_symbol())
                    db.reset_conditions()
                elif db.get_head() == 1:
                    db.inc_count()
            else:
                db.reset_conditions()
        else:
            if message.from_user.id == KATRINA_ID:
                if 'привет' in message.text or 'Привет' in message.text:
                    await app.send_message(chat_id=KATRINA_ID, text=PHRASES[random.randrange(1, len(PHRASES) - 1)])
                elif 'спать' in message.text or 'Спать' in message.text or 'спишь' in message.text or 'Спишь' in message.text:
                    text = 'я не могу без тебя спать ❤️'
                    await app.send_message(chat_id=KATRINA_ID, text=text)
            elif message.from_user.id == TTARGET_ID:
                await app.send_message(chat_id=TTARGET_ID, text=f'{"".join(random.choice(string.ascii_letters + string.digits + string.hexdigits) for _ in range(16, 64))}')

try:
    app.run()
except Exception as error:
    print(error)


