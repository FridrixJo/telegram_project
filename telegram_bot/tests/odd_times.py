def find_odd(seq: list):
    diction = {}
    for i in seq:
        diction[i] = 0

    for i in seq:
        diction[i] += 1

    for i in diction:
        if diction[i] % 2 == 1:
            return i


print(find_odd([20,1,-1,2,-2,3,3,5,5,1,2,4,20,4,-1,-2,5]))


def find(seq: list):
    for i in seq:
        if seq.count(i) % 2 == 1:
            return i


print(find([20,1,-1,2,-2,3,3,5,5,1,2,4,20,4,-1,-2,5]))
