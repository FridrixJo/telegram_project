#!/usr/bin/python
# -*- coding: utf8 -*-

from tests.get_authorized import Api_Data
from aiogram_bot.main_script import Script
from data_basesp.db import AccountsDB

db = AccountsDB('../data_base/accounts.db')
#   Phone = '79658044563'
#   Phone = '79604610785'
#   Phone = '79852059341'
Phone = '79264892749'

#   Phone = '79852059341'

if not db.account_exists(Phone):
    data = Api_Data(Phone)
    data.login()

    db.add_phone_number(Phone)

else:
    Id = db.get_api_id(Phone)
    Hash = db.get_api_hash(Phone)

#Id = 16099912
#Hash = 'db042e346eb9569f9a6392cbbae05ace'
#Phone = '79264892749'
CHAT_LINK = 'https://t.me/joinchat/oupOR2wLRYoxM2Q6'

session_name = Phone

login = Script(session_name=session_name,
                  api_id=Id,
                  api_hash=Hash,
                  phone_number=Phone,
                  chat_link=CHAT_LINK,
                  data='hola')


login.start()


