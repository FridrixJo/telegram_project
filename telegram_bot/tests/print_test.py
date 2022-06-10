from pyrogram import Client
from scripts.get_authorized import Api_Data

#api = Api_Data()
#params = api.login('79117946323')

#ID = params[0]
#HASH = params[1]
#PHONE = params[2]

ID = 13467303
HASH = '16e8112f104c345b655f1fdbb5d31208'
PHONE = '79117946323'

CHAT_LINK = 'https://t.me/joinchat/oupOR2wLRYoxM2Q6'

print(PHONE)

if __name__ == '__main__':
    try:
        app = Client(name=PHONE, api_id=ID, api_hash=HASH, phone_number=PHONE)
        #app.start()
        app.connect()
        app.send_code(PHONE)
        send_code = app.send_code(PHONE)
        print(send_code)
        code = input("code? ... ")
        signed_in = app.sign_in(PHONE, send_code.phone_code_hash, code)
        app.send_message('me','ola-la')
        app.disconnect()
    except Exception as e:
        print(e)
