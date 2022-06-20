#!/usr/bin/python
# -*- coding: utf8 -*-
import pyrogram.errors.exceptions.bad_request_400
from pyrogram import Client
from pyrogram.enums import UserStatus, ChatMemberStatus, SentCodeType, ChatMembersFilter
from pyrogram.types import SentCode
from pyrogram.errors import SessionPasswordNeeded

from pyrogram.types import Chat, ChatPreview

import time
import random

import threading

import asyncio
from asyncio import set_event_loop, new_event_loop


class Script:
    def __init__(self, session_name, api_id, api_hash, phone_number, chat_link, data):
        self.app = Client(name=session_name, api_id=api_id, api_hash=api_hash, phone_number=phone_number)
        self.data = data
        self.chat_link = chat_link
        self.phone = phone_number
        self.send_code: SentCode
        self.x = threading.Thread

    def change_chat_link(self, chat_link):
        self.chat_link = chat_link

    def change_data(self, data):
        self.data = data

    async def resend_code(self):
        try:
            phone_code_hash = self.send_code.phone_code_hash
            self.send_code = await self.app.resend_code(phone_number=self.phone, phone_code_hash=phone_code_hash)
        except Exception as e:
            print(e)
            print(type(e))
            return False, e

        return True, 'OK'


    async def verify(self):
        try:
            await self.app.connect()
            await asyncio.sleep(1)
            self.send_code = await self.app.send_code(self.phone)
        except Exception as e:
            print(e)
            print(type(e))
            return False, e

        return True, 'OK'

    async def input_code(self, telegram_code: SentCodeType):
        print(self.send_code)
        if self.send_code.type == SentCodeType.APP:
            code = telegram_code
            try:
                #set_event_loop(asyncio.new_event_loop())
                #loop = asyncio.get_event_loop()
                #future = asyncio.ensure_future(self.app.sign_in(self.phone, str(self.send_code.phone_code_hash), str(code)), loop=loop)
                #loop.run_until_complete(future)
                #time.sleep(3)
                #x = threading.Thread(target=self.app.sign_in, args=(self.phone, str(self.send_code.phone_code_hash), str(code),), daemon=True)
                #x.start()
                #x.join()

                #set_event_loop(asyncio.new_event_loop())
                #loop = asyncio.get_event_loop()

                #future = asyncio.ensure_future(coro_or_future=self.app.sign_in(self.phone, str(self.send_code.phone_code_hash), str(code)), loop=loop)
                #loop.run_until_complete(future=future)

                #task = asyncio.create_task(coro=self.app.sign_in(self.phone, str(self.send_code.phone_code_hash), str(code)), name='qwerty')
                #await task

                await self.app.sign_in(self.phone, str(self.send_code.phone_code_hash), str(code))

                return True, 'OK'
            except Exception as e:
                print(type(e))
                print(e)
                print(e.args)
                print('input code')
                return False, e
        else:
            return False, 'Код не отправляется в Telegram из-за ограничений вашего акканута, попробуйте позже'

    async def start(self):

        print(self.app)

        try:
            chat = await self.app.get_chat(self.chat_link)
        except Exception as e:
            print(e, "getting chat")
            return

        members = []

        if type(chat) == Chat:
            async for i in self.app.get_chat_members(chat_id=chat.id, limit=150, filter=ChatMembersFilter.RECENT):
                try:
                    members.append(i)
                except Exception as e:
                    print(e, "adding members to list from chat")
            print(len(members))
        else:
            return 0

        count = 0
        for i in members:
            await asyncio.sleep(random.randrange(2,3))

            try:
                print(i.status)
                print(await self.app.get_chat_history_count(i.user.id))
                print(i.user.status)
            except Exception as e:
                print(e)
                continue

            if i.status == ChatMemberStatus.MEMBER and i.user.is_contact is False and await self.app.get_chat_history_count(i.user.id) == 0 and i.user.is_deleted is False and i.user.status != UserStatus.LONG_AGO and i.user.status != UserStatus.LAST_MONTH and i.user.status != UserStatus.LAST_WEEK:
                try:
                    await self.app.send_message(i.user.id, self.data)
                    count += 1
                except pyrogram.errors.exceptions.bad_request_400.PeerFlood as e:
                    try:
                        await self.app.disconnect()
                    except Exception as e:
                        print(e, 'log_out')

                    print('qwertyuiop')
                    return count
                except Exception as e:
                    print(e, "sending message to members from chat")
                    print(type(e))
        print(count)

        try:
            await self.app.disconnect()
        except Exception as e:
            print(e, 'log_out')
        return count



