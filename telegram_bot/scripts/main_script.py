#!/usr/bin/python
# -*- coding: utf8 -*-

from pyrogram import Client
from pyrogram.enums import UserStatus, ChatMemberStatus, SentCodeType
from pyrogram.errors import SessionPasswordNeeded

import time
import random

class Script:
    def __init__(self, session_name, api_id, api_hash, phone_number, chat_link, data):
        self.app = Client(name=session_name, api_id=api_id, api_hash=api_hash, phone_number=phone_number)
        self.chat_link = chat_link
        self.data = data
        self.phone = phone_number

    def change_params(self, chat_link, data):
        self.chat_link = chat_link
        self.data = data

    def verify(self):
        self.app.connect()
        self.app.send_code(self.phone)
        send_code = self.app.send_code(self.phone)
        print(send_code)
        if send_code.type == SentCodeType.APP:
            code = input("code? ... ")

            try:
                signed_in = self.app.sign_in(self.phone, send_code.phone_code_hash, code)
                return True
            except Exception as e:
                print(e)
                return False
        return False


    def check_session(self):
        pass


    def start(self):
        #self.verify()
        try:
            print(self.app.export_session_string())
            self.app.start()
        except Exception as e:
            if self.verify() is not True:
                return

        print(self.app.get_contacts())

        print(self.app.export_session_string())

        try:
            chat = self.app.get_chat(self.chat_link)
        except Exception as e:
            print(e, "getting chat")
            return

        members = []
        for i in self.app.get_chat_members(chat.id):
            try:
                members.append(i)
            except Exception as e:
                print(e, "adding members to list from chat")
        print(len(members))

        count = 0
        for i in members:
            time.sleep(random.randrange(2,4))
            print(i.status)
            print(self.app.get_chat_history_count(i.user.id))
            print(i.user.status)
            if i.status == ChatMemberStatus.MEMBER and i.user.is_contact == False and self.app.get_chat_history_count(i.user.id) == 0 and i.user.is_deleted == False:
                # and i.user.status != UserStatus.LONG_AGO and i.user.status != UserStatus.LAST_MONTH and i.user.status != UserStatus.LAST_WEEK:
                try:
                    self.app.send_message(i.user.id, self.data)
                    count += 1
                except Exception as e:
                    print(e, "sending message to members from chat")
        print(count)

        return count



