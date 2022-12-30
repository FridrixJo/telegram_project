s = """
4).
 e662b8ce225a47fc01cbabe0de2cb27b

20813104

+12269408275

1641416805
"""

x = s.split('\n')
new_arr = []
for i in x:
    if len(i) > 6:
        new_arr.append(i.strip())

print(new_arr)

