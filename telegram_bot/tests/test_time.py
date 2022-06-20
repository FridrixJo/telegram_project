import time

time1 = time.time()
print(time1/(3600*24))

time.sleep(10)

time2 = time.time()

print(time2 - time1)
