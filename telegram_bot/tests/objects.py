class A:

    def __init__(self):
        self.n = 5

    def __str__(self):
        return str(self.n)


a = A()
b = a
b.n = 150
print(b)
print(a)
