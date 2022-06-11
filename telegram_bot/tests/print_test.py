from pyrogram import Client
from scripts.get_authorized import Api_Data
from scripts.main_script import Script

#api = Api_Data()
#params = api.login('79117946323')

#ID = params[0]
#HASH = params[1]
#PHONE = params[2]

ID = 10619800
HASH = 'be3ad66a73535e071d9ab3347404a30b'
PHONE = '+79670170740'

CHAT_LINK = 'https://t.me/joinchat/oupOR2wLRYoxM2Q6'


if __name__ == '__main__':
    machine = Script(session_name=PHONE, api_id=ID, api_hash=HASH, phone_number=PHONE, chat_link=CHAT_LINK, data='privet')

    if machine.get_session() is False:
        machine.verify()
        code = input('code? ...')
        machine.input_code(code)
        machine.start()
    else:
        machine.start()
