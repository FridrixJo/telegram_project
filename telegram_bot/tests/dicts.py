import string
import random

for i in range(0):
    short_name = ''.join(random.choice(string.digits + string.ascii_letters) for _ in range(random.randrange(16, 64)))
    a = '849764'
    dict = {'data':[short_name, a]}
    print(dict['data'])
