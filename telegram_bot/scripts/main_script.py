#!/usr/bin/python
# -*- coding: utf8 -*-
import pyrogram.errors.exceptions.bad_request_400
from pyrogram import Client
from pyrogram.enums import UserStatus, ChatMemberStatus, SentCodeType, ChatMembersFilter
from pyrogram.types import SentCode

from pyrogram.types import Chat, ChatPreview

import random

import asyncio


class Script:
    def __init__(self, session_name, api_id, api_hash, phone_number, chat_link, data):
        self.app = Client(name=session_name, api_id=api_id, api_hash=api_hash, phone_number=phone_number)
        self.data = data
        self.chat_link = chat_link
        self.phone = phone_number
        self.send_code: SentCode
        self.members = []

    def get_phone(self):
        return self.phone

    async def get_account_name(self):
        user: pyrogram.types.User
        user = await self.app.get_me()
        text = ''
        first_name = user.first_name
        last_name = user.last_name
        if first_name is not None:
            text += first_name + ' '
        if last_name is not None:
            text += last_name

        return text

    async def get_account_username(self):
        user: pyrogram.types.User
        user = await self.app.get_me()
        text = ''
        username = user.username
        if username is not None:
            text += username

        return username

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

    async def get_chat_members(self):

        print(self.app)

        try:
            chat = await self.app.get_chat(self.chat_link)
        except Exception as e:
            print(e, "getting chat")
            return False, e

        self.members = []

        if type(chat) == pyrogram.types.Chat:
            async for i in self.app.get_chat_members(chat_id=chat.id, limit=150, filter=ChatMembersFilter.RECENT):
                try:
                    self.members.append(i)
                except Exception as e:
                    print(e, "adding members to list from chat")
            print(len(self.members))
        else:
            return False, 'private chat'

        return True, 'OK'

    async def write(self):
        count = 0
        for i in self.members:
            await asyncio.sleep(random.randrange(2, 3))
            if i.status == ChatMemberStatus.MEMBER and i.user.is_contact is False and await self.app.get_chat_history_count(i.user.id) == 0 and i.user.is_deleted is False and i.user.status != UserStatus.LONG_AGO and i.user.status != UserStatus.LAST_MONTH and i.user.status != UserStatus.LAST_WEEK:
                try:
                    await self.app.send_message(i.user.id, self.data)
                    print('count', self.phone)
                    count += 1
                except pyrogram.errors.exceptions.bad_request_400.PeerFlood as e:
                    try:
                        await self.app.disconnect()
                    except Exception as e:
                        print(e)

                    print('account got spam')
                    return count, 'LIMITED'

                except Exception as e:
                    print(e, "sending message to members from chat")
                    print(type(e))
            else:
                print('skipped', self.phone)

        try:
            await self.app.disconnect()
        except Exception as e:
            print(e)

        return count, 'ALL_PEOPLE_PASSED'



