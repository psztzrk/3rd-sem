# Staticmethod

class MathUtils:
    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def is_even(number):
        return number % 2 == 0


print(MathUtils.add(2, 3))
print(MathUtils.is_even(10))

# Class method és copy constructor
import copy


class AdvancedStack:

    def __init__(self, data=None):
        self._data = list(data) if data else []

    @classmethod
    def from_stack(cls, other: AdvancedStack):
        """
        Copy constructor (shallow copy) A cls nem futtatja az __init__()-et, ha csak nem hívjuk explicit meg
        """
        cls._data = other._data
        return cls

    def clone_deep(self):
        """
        Deep copy a copy modullal
        """
        # Látjuk, hogy a self-et használja -> Példányon dolgozik nem a classon
        return AdvancedStack(copy.deepcopy(self._data))  # Ilyen, amikor valami nem classmethod hanem instance method

    @classmethod
    def from_list(cls, lst):  # Pl. a pandasnál fogunk majd ilyeneket látni
        return cls(lst)

    @classmethod
    def from_tuple(cls, tpl):
        return cls(list(tpl))

    @classmethod
    def empty(cls):
        return cls()


s1 = AdvancedStack([[1], [2]])
s2 = s1.clone_deep()
s3 = s1.from_stack(s1)

s1._data[0].append(99)

print('Eredeti:', s1._data)
print('Deep copy másolat:', s2._data)
print('Shallow copy másolat:', s3._data)

s3 = AdvancedStack.from_list([1, 2, 3])
s4 = AdvancedStack.from_tuple((4, 5))
s5 = AdvancedStack.empty()

print('Alterantív konstruktorok:', s3._data, s4._data, s5._data)

# A classmethodok hívása:

s = AdvancedStack([1, 2, 3])

# Így szoktuk
copy1 = AdvancedStack.from_stack(s)

# Így is lehet hívni, nem explicit
copy2 = s.from_stack(s)

print('Classmethod hívása:', copy1._data, copy2._data)

# Getitem és setitem

class IndexedStack(AdvancedStack):

    def __getitem__(self, index):
        """Indexelés olvasásra: stack[0]"""
        return self._data[index]

    def __setitem__(self, index, value):
        """Indexelés irásra értékadással: stack[0] = 10"""
        self._data[index] = value


idx_stack = IndexedStack([10, 20, 30])
print(idx_stack[1])

idx_stack[1] = 99
print(idx_stack._data)

# Contextmanager class formában -> Ilyet csinál a generátorból a @contextmanager dekorátor

class ManagedStack(AdvancedStack):

    def __enter__(self):
        print('Entering context (resource acquired)')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print('Exiting context (resource released)')
        """
        if exc_type is not None:
            print('Exception detected:', exc_type, exc_value)

            # True elnyomjuk az exceptiont
            return True
        """
        print('No exception occurred')
        return False  # False-sal propagáljuk


with ManagedStack([1, 2, 3]) as ms:
    ms._data.append(4)
    print(ms._data)
    print('Inside context')
    # raise ValueError('Something went wrong')  # Ő el van nyomva, megy tovább a futtatás (az IDE ezt nem látja)


# Adatbázisos példa contexmanagerre

class DatabaseConnection:

    def __enter__(self):
        print('Connecting to database...')
        self.connected = True
        return self

    def query(self, sql):
        if not self.connected:
            raise RuntimeError('Not connected')
        print(f'Executing: {sql}')

    def __exit__(self, exc_type, exc_value, traceback):
        print('Closing database connection...')
        self.connected = False

        if exc_type:
            print('Rolling back transaction due to error')
        else:
            print('Committing transaction')


with DatabaseConnection() as db:
    db.query('SELECT * FROM users')

# Abstract base class:
# Ezeket nem lehet közvetlenül példányosítani
# Ezek az alosztályokban bizonyos metódusok megvalósítását írják elő

from abc import ABC, abstractmethod


class AbstractContainer(ABC):

    @abstractmethod
    def add(self, item):  # Kötelező method és a subclass páldányosításnál ellenőrződik
        pass

    def remove(self):  # Opcinonális method és a subclass methodjának hívásakor ellenőrződik
        raise NotImplementedError


class ConcreteStack(AbstractContainer):

    def __init__(self):
        self._data = []

    def add(self, item):
        self._data.append(item)

    def remove(self):
        return self._data.pop()

cs = ConcreteStack()
cs.add(10)
print(cs.remove())


# Kompozíció vs. öröklődés
# Öröklődés: IS-A kapcsolat
# Kompozíció: HAS-A kapcsolat


class Storage:
    def __init__(self):
        self.data = []


class ComposedStack:
    def __init__(self):
        self.storage = Storage()  # Kompozíció nem öröklődés!

    def push(self, value):
        self.storage.data.append(value)

    def pop(self):
        return self.storage.data.pop()


comp_stack = ComposedStack()
comp_stack.push(5)
print(comp_stack.pop())

# A dataclassok csökkentik a sablonos kód mennyiségét
# Automatikusan létrehozza az __init__, __repr__ és __eq__ metódusokat

from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int


p1 = Point(1, y=2)  # -> (1, 2), NamedTuple(x=1, y=2)
p2 = Point(1, 2)

print(p1)
print('Equality:', p1 == p2)

# Property, getter, setter

class Temperature:

    def __init__(self, celsius):
        self._celsius = celsius

    @property
    def celsius(self):  # Ez a getter
        return self._celsius

    @celsius.setter
    def celsius(self, value):  # Ez a setter
        if value < -273.15:
            raise ValueError('Below absolute zero!')
        self._celsius = value

    @property
    def fahrenheit(self):  # Nincs setter -> read only property
        return (self._celsius * 9 / 5) + 32


t = Temperature(25)
print(t.celsius)
print(t.fahrenheit)

t.celsius = 30
print(t.celsius)
print(t.fahrenheit)

try:
    t.fahrenheit = 30
except AttributeError:
    print('Ez biza atribute error')


# ORM (OBJECT RELATIONAL MAPPING) -> pl. Adatbázis táblák és rekordok objektumoként való kezeléséhez
#     Tábla -> Class
#     sor/rekord   -> Object
#     oszlop -> Attribute

# A class definíció SQL sémává alakítható

class User:
    def __init__(self, id_, name):
        self.id = id_
        self.name = name

    def save(self):
        print(f'INSERT INTO users VALUES ({self.id}, "{self.name}")')  # Mintha mentenénk az adatbázisba

    @classmethod
    def get(cls, id):
        print(f'SELECT * FROM users WHERE id={id}')  # Mintha az adatbázisból származna az adat
        return cls(id, 'MockUser')


user = User(1, 'Alice')
user.save()

fetched = User.get(1)
print(fetched.name)
