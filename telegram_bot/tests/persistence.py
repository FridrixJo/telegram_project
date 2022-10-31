def persistence(n: int):
    s = str(n)
    num = 1
    count = 0
    while(len(s) != 1):
        for i in s:
            num *= int(i)
        count += 1
        s = str(num)
        num = 1

    return count


print(persistence(999))
