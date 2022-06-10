from pyrogram import Client

Id = 16099912
Hash = 'db042e346eb9569f9a6392cbbae05ace'
Phone = '79264892749'

proxy = {
    "scheme": "socks5",
    "hostname": "217.29.53.104",
    "port": 12243,
    "username": "9vjSgf",
    "password": "4mTD2v"
}

bot = Client(name=Phone, api_id=Id, api_hash=Hash, proxy=proxy)

bot.connect()
send_code = bot.send_code(Phone)

code = input("code? ...")

signed_in = bot.sign_in(Phone, send_code.phone_code_hash, code)

bot.send_message('me', 'hey, that\'s me')
bot.disconnect()
