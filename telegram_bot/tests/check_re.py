import re

link = 'https://t.me/chats_piar'
reg = r'(https://t.me/)(.+)'
x = re.search(reg, link)

print(x.start())
