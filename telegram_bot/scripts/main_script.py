#!/usr/bin/python
# -*- coding: utf8 -*-

from pyrogram import Client
from pyrogram.enums import UserStatus, ChatMemberStatus, SentCodeType
from pyrogram.errors import SessionPasswordNeeded

from pyrogram.types import Chat, ChatPreview

import time
import random

import asyncio
from asyncio import set_event_loop, new_event_loop

class Script:
    def __init__(self, session_name, api_id, api_hash, phone_number, chat_link, data):
        self.app = Client(name=session_name, api_id=api_id, api_hash=api_hash, phone_number=phone_number)
        self.data = data
        self.chat_link = chat_link
        self.phone = phone_number
        self.send_code = ''

    def change_chat_link(self, chat_link):
        self.chat_link = chat_link

    def change_data(self, data):
        self.data = data

    def verify(self):
        try:
            self.app.connect()
            self.send_code = self.app.send_code(self.phone)
        except Exception as e:
            return False

        return True

    def input_code(self, telegram_code):
        print(self.send_code)
        try:
            if self.send_code.type == SentCodeType.APP:
                code = telegram_code

                try:
                    print(66666666666666666)
                    signed_in = self.app.sign_in(self.phone, self.send_code.phone_code_hash, code)
                    print(self.app.export_session_string())
                    return True
                except Exception as e:
                    #self.app.disconnect()
                    print(e)
                    return False
            else:
                print(1)
                self.app.disconnect()
                return False
        except Exception as e:
            print(e)
            return False



    def get_session(self):
        try:
            print(self.app.export_session_string())
            self.app.start()
            return True
        except Exception as e:
            print(e)
            return False



    def start(self):

        try:
            chat = self.app.get_chat(self.chat_link)
        except Exception as e:
            print(e, "getting chat")
            return

        members = []

        if type(chat) == Chat:
            list_of_members = self.app.get_chat_members(chat_id=chat.id, limit=50)
            for i in list_of_members:
                try:
                    members.append(i)
                except Exception as e:
                    print(e, "adding members to list from chat")
            print(len(members))
        else:
            return 0

        count = 0
        for i in members:
            time.sleep(random.randrange(2,4))
            print(i.status)
            print(self.app.get_chat_history_count(i.user.id))
            print(i.user.status)
            if i.status == ChatMemberStatus.MEMBER and i.user.is_contact == False and self.app.get_chat_history_count(i.user.id) == 0 and i.user.is_deleted == False and i.user.status != UserStatus.LONG_AGO and i.user.status != UserStatus.LAST_MONTH and i.user.status != UserStatus.LAST_WEEK:
                try:
                    self.app.send_message(i.user.id, self.data)
                    count += 1
                except Exception as e:
                    print(e, "sending message to members from chat")
        print(count)

        return count



