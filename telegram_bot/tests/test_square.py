def square_digits(num):
    sum = ''
    for i in str(num):
        sum += str(pow(int(i), 2))
    return int(sum)


def square_digits2(num):
    return int(''.join(str(int(i)**2) for i in str(num)))


print(square_digits(9119))
print(square_digits2(9119))
