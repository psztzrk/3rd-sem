# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


a = str(1)
b = int(1)
c = float(1)
d = bool(1)
e = None

print(7 / 3, type(7 / 3))
print(7 // 3, type(7 // 3))
print(7 % 3, type(7 % 3))
print(7 ** 3, type(7 ** 3))
print(9.0 / 3)
print(9 / 3.0)

def nev():   #  ez egy függvény
    print("Ez egy fgv")

nev()   #  így van meghívva
def nev2(a, b, c=2):
    print(a, b, c)

nev2(1,2,3)
nev2(1,2)
nev2(a,b,4)
z = 2
def nev2(a =3, b = None, c=2):

    #  z = 3   ez így nincs definiálva a függvényen kívűl
    global z
    z = 3
    print(a, b, c)

nev2(b = 3, c = 4, a = 2)

nev2 = int
print(z)
nev2('1')

#  nev2.__call__()

print(1,2,3)

import sys

print(1, '2', 3.0, None, False, sep=',', end='\n\n')   #  a default separator value egy space, de állítható

print(1, '2', 3.0, None, False, sep=',', end='\n', file=sys.stderr, flush=False)

print('ok')

start = 0
step = 2
stop = 10

print(list(range(start, stop, step)))

print(3 not in range(start, stop, step))

r = range(10)
print(r.start)
print(list(r))

a = [1,2,3]
b = (4,5,6)
c = {7,8,9}

a.append(4)
print(a)
a.insert(1, 5)
print(a)

##  print(a.index(30))  #  eezz nincs is benne -> value error
print(341 in a)
print(341 in b)
print(342 in c)

c.add(23)
print(c)

t = tuple([1,2,3])
l = list([1,2,3])
l2 = list(t)
s = set([1,2,3])
g = ([1,2,3,])  #   ugyanez működik listával is
g = ([
    1,  #  adfg
    2,  #  ez azért jó mert lehet kommentelni
    3,
])

j = []  #  üres lista
k = ()  #  üres tuple
l = {}  #  ez nem az üres halmaz

def fun(*a):
    print(a)

fun(1,2,3)

d = dict()  #  avagy {} ezért a set()-tel definiálunk üres halmazt

r = {(1,2,3): [2], 3: {1,3,3}}




## blalaaa

lc = (x*x for x in range(10) if x % 2 == 0)

for e in lc:
    print(e)

from itertools import repeat, cycle, islice, accumulate
a = accumulate(range(10))
print(list(a))

from itertools import groupby
