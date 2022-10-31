def descending_irder(num: int):
    x = []
    str_num = str(num)
    print(str_num)
    for i in str_num:
        x.append(i)

    x.sort()
    x.reverse()

    number = 0

    for i in range(len(x)):
        number += int(x[i]) * pow(10, len(x) - 1 - i)

    return number


print(descending_irder(15))


def descending_order2(num: int):
    return int(''.join(sorted(str(num), reverse=True)))


print(descending_order2(14))

x = ['a','b','c','d']

a = 'TWIMS'.join(x)
print(a)
