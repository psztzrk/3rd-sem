class Stack:
    """Verem osztály"""
    created_stacks = 0  # Static attribútum minden objektummal közös

    def __init__(self, initial=None):
        """Konsturktor, self, copy konstruktor, rejtett metódusok"""

        self._data = []  # Protected attributum. Az IDE szól ha kívülről van használva

        self.__secret_counter = 0  # Privát attributum, _Stack__secret_counter néven kerül tárolásra

        if initial is not None:
            self._data.extend(initial)

        Stack.created_stacks += 1

    def __del__(self):
        """Destruktor, általában nincs rá szükség, mert a GC elintézi -> Azért el lehet leakelni a memóriát vele
           -> Kontext menedzserek alkalmazása
        """
        pass

    # API
    def push(self, value):
        self._data.append(value)

        self._increment_counter()

    def pop(self):
        return self._data.pop()

    def peek(self):
        return self._data[-1]

    def is_empty(self):
        return len(self._data) == 0

    # Protected method, belső használatra
    def _increment_counter(self):
        self.__secret_counter += 1

    # Privát method -> _Stack__internal_state()
    def __internal_state(self):
        return f'Internal pushes: {self.__secret_counter}'

    # 'Magic methods'
    def __len__(self):  # -> len(stack)
        return len(self._data)

    def __eq__(self, other: object):  # -> stack1 == stack2
        if not isinstance(other, Stack):
            return NotImplemented

        return self._data == other._data

    def __gt__(self, other):  # -> stack1 > stack2
        if not isinstance(other, Stack):
            return NotImplemented  # Itt nem raise és NotImplementedError van!

        return len(self) > len(other)

    def __lt__(self, other):
        return NotImplemented  # Figyeljük meg a returnt!

    def __hash__(self):  # -> hash(stack)
        return hash(tuple(self._data))

    def __str__(self):  # -> str(stack)
        return f'Stack(top -> {list(reversed(self._data))})'

    def __repr__(self):  # -> repr(stack)  -> eval()-ban kóddá alakítható a koncenció szerint
        return f'Stack({self._data})'

## Pár rejtett attributum

# Name of the class
print('Class name:', Stack.__name__)

# Module where class is defined
print('Module:', Stack.__module__)

# Parent classes
print('Base classes:', Stack.__bases__)

# Dictionary of attributes and methods
print('Class dictionary keys:')
print(list(Stack.__dict__.keys()))

# Itt érdemes megfigyelni a __doc__ -ot, ami a help(stack) -al érhető el amúgy
# help(Stack)

# Használat

s1 = Stack([1, 2, 3])

s1.push(4)
s1.push(5)

print(s1)
print('Top:', s1.peek())
print('Length:', len(s1))

s2 = Stack(s1._data)

print('Copied stack:', s2)

print('Equality:', s1 == s2)

s2.pop()

print('Greater comparison:', s1 > s2)

# Ez mégis működik, hiába NotImplemented -> Kikövetkezteti a meglévőkből! Csak azonos típus hasonlítása esetn működik!
# Lásd még @total_ordering később...
print('Less comparison:', s1 < s2)

print('Hash values:')
print(hash(s1), hash(s2))

print('Csak a konvenció tiltja a hozzáférést:', s1._data)

try:
    print(s1.__secret_counter)  # AttributeError
except AttributeError:
    print('Ez bizony attribute error')

print('De "name mangling"-gel:')
print(s1._Stack__secret_counter)


class LimitedStack(Stack):
    def __init__(self, capacity, initial=None):
        super().__init__(initial)  # A baseclass konstruktorát ez hívja meg, enélkül nem fut le -> ABC-t lehet csinálni
        self.capacity = capacity

    def push(self, value):  # Szó nélkül overload-olja a metódust
        if len(self._data) >= self.capacity:
            raise OverflowError('Stack capacity exceeded')

        super().push(value)  # Ha a szülő metódusát akarjuk használni


# A subclass használata
ls = LimitedStack(3)

ls.push(10)
ls.push(20)
ls.push(30)

print(ls)

try:
    ls.push(40)
except OverflowError as e:
    print('Exception:', e)

# Statikus attributum tényleg statikus
print('Stacks created:', Stack.created_stacks)


s3 = Stack()

print('Stacks created:', Stack.created_stacks)


# Többszörös öröklődés

# A Mixin-ek előre legyártott építőkockák, amiket örökléssel lehet felhasználni
# -> Kevesebb saját kód az egyértelmű részeknél pl. interfaceek implelementálása...
class LoggingMixin:
    def log(self, message):
        print(f'[LOG]: {message}')


class IterableMixin:
    def __iter__(self):
        for item in self._data:
            yield item


class AdvancedStack(Stack, LoggingMixin, IterableMixin):
    def push(self, value):
        self.log(f'Pushing {value}')
        super().push(value)

adv = AdvancedStack([1, 2, 3])
adv.push(4)

for x in adv:
    print('Iterated:', x)

# Metódusok feloldási sorrendje
print('MRO:', AdvancedStack.mro())


# Rendezési operátorok

from functools import total_ordering


@total_ordering  # -> Ezzel a __eq__ + még egy függvényből megcsinálja az __lt__, __le__, __gt__, __ge__ négyest
class OrderedNumber:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other: object):
        if not isinstance(other, OrderedNumber):
            return NotImplemented
        return self.value == other.value

    def __lt__(self, other):
        if not isinstance(other, OrderedNumber):
            return NotImplemented
        return self.value < other.value

a = OrderedNumber(5)
b = OrderedNumber(10)

print(a < b)
print(a <= b)
print(a > b)
print(a >= b)

# Kezdő hibák...

class BadEquality:

    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value  # Nincs isinstance, tehát nem biztos, hogy van .value -> AttributeError

x = BadEquality(5)

class SomethingElse:
    def __init__(self):
        self.value = 5


y = SomethingElse()

print('Más típussal is működik, amíg tud:', x == y)

# Ha nem vagyunk biztosak, akkor ellenőrizni kell -> De ez többnyire rossz designt jelent

s = Stack([1, 2, 3])

print('Has attribute "_data":', hasattr(s, '_data'))

data = getattr(s, '_data')
print('Data via getattr:', data)

setattr(s, 'debug_mode', True)

print('New attribute:', s.debug_mode)


# Hashing hibák... Ha két objektum azonos tpíusú és az értéke is azonos, akkor a hash-je is azonos kell, hogy legyen

class BadHash:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other: object):
        return isinstance(other, BadHash) and self.value == other.value

    def __hash__(self):
        return id(self)  # Hiba -> különböző obj-ok mindig más ID-t kapnak, de attól még lehet azonos az értékük

a = BadHash(10)
b = BadHash(10)

print('Equality:', a == b)
print('Hash a:', hash(a))
print('Hash b:', hash(b))


class GoodHash:

    def __init__(self, value):
        self.value = value

    def __eq__(self, other: object):
        return isinstance(other, GoodHash) and self.value == other.value

    def __hash__(self):
        # A belső értékek, amik a hash alapját képezik az egyelőségvizsgálatnál használtak leggyenek!
        return hash(self.value)


c = GoodHash(10)
d = GoodHash(10)

print('Equality:', c == d)
print('Hash c:', hash(c))
print('Hash d:', hash(d))


# Dekorátorok

def logger(func):
    def wrapper(*args, **kwargs):
        print(f'Függvény meghívva: {func.__name__}')

        result = func(*args, **kwargs)

        print(f'Függvény véget ért: {func.__name__}')
        return result

    return wrapper


@logger  # Gyakorlatilag add = logger(add)
def add(a, b):
    return a + b

print(add(2, 3))

# Ez mást mond mint gondolnánk -> wraps!
print(add.__name__)
print(add.__doc__)

from functools import wraps

def debug(function=None, *, level=1):
    def decorator(original_function):
        @wraps(original_function)
        def wrapper(*args, **kwargs):
            print(f'[DEBUG level={level}] {original_function.__name__}')
            res = original_function(*args, **kwargs)
            print('[UTÁNA DEBUG]')
            return res

        return wrapper

    if function is None:  # Ha nincs paramétere a dekorátornak: debug(level=3)(function)
        return decorator

    return decorator(function)  # Ha van paramétere a dekorátornak: debug(function)


@debug
def foo():
    print('foo')


@debug(level=3)
def bar():
    print('bar')

from functools import lru_cache

# Praktikusan:
@lru_cache(maxsize=None)
def fun2():
    print('valami2')

