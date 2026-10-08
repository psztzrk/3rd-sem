def prefixalt_stringek():
    # A macskaköröm és aposztróf csereszabatos, így csak az egyikkel mutatom be a lehetőségeket a továbbiakban
    s = 'ékezetek:áő'  # str()   Sima string: Karakter alapú teles Unicode paletta használható
    b = b'bytestring'  # bytes() Byte string: Byte alapú. Csak ASCII karakterek és escapek használhatók!
    # b2 = b'űáéúő'    # SyntaxError
    print(type(b))     # bytes típus nem str
    print(type(s.encode('UTF-8')))  # bytes() -> str() Vigyázni kell a karakterkódolással! Mojibake, stb.
    print(type(b.decode('UTF-8')))  # str() -> bytes()

    r = r'dsfs\ndf'              # Raw string: a \ alapból literális értemű -> Regexeknél hasznos, átláthatóbb
    print(r, 'vs.', 'dsfs\ndf')  # A sima stringnél a \-t escapelni kell
    f = f'cmike: {r}'  # Format string: Különféle formázásokat lehet belerakni: f'{expression:format_spec}'
    print(f, f'{{valami}}', f'Két tizedesre kerekítve: {10/3:.2f}', f'Pontosan három számjegy{7:03d}')
    print(f'Ezres elválasztó: {1234567:,}', f'Százalék: {0.756:.1%}')
    name = '123'
    width = 10

    # Tabulálás és vizszintes rendezés
    print(f'|{name:<10}|')  # bal 10 széles cellában
    print(f'|{name:^10}|')  # közép
    print(f'|{name:>{width}}|')  # jobb

    text = 'hello\nworldúőűáéű'
    print(f'{text!r}')  # repr()  -> Dev barát megjelenítés pl újsor escapelve
    print(f'{text!s}')  # str()   -> Ahogy megjelenne az usernek stringként
    print(f'{text!a}')  # ascii() -> Csak ASCII karakterek felhasználásával

    # Dátumformázás
    from datetime import datetime
    print(f"{datetime.now():%Y-%m-%d %H:%M}")


def alap_string_muveletek():
    # A str egy immutable sequence típus, akárcsak a tuple, de karakterekre specializálva, saját műveletekkel
    # Közös: Hossz, indexelés/sliceolás, in, konkatenáció, ismétlés (pl. s * 3), index, count
    s = 'string'
    t = ('s', 't', 'r', 'i', 'n', 'g')
    print('alma'.count('a'))         # Megszámolja az egyező elemeket
    print(s.index('r'))              # Substring indexe a stringben
    print(s.index('r', 1, -1))       # Opcionálisan leszűkítve a keresés kezdeti és vég indexeit
    print(t.index('r',1, -1))        # A tuple/listával is működik
    # print(s.index('f'))            # Ez value eror-t ad mert nincs a stringben ilyen substring
    print(s.find('f'))               # Ez -1-et ad ha nem talál semmit
    # print(t.find('t'))             # Find csak a str típusnál van!

    # Csak str
    print(s.startswith('pre'))       # Prefixet vizsgál. Ha tuple-t kap több alternatívát is képes megnézni
    print(s.endswith(('s', 'a')))    # Sufixet vizsgál. Ha tuple-t kap több alternatívát is képes megnézni

    s2 = 'alma körte  dinnye '
    print(s2.split())                 # Speciálisan működik: az egymás utáni spaceket egyben kezeli, nincs üres a végén
    print(s2.split(' '))              # Ez konkrétan a megadott karakternél vág
    print(s2.split(' ', maxsplit=2))  # Meg lehet adni maximum vágási számot
    print(''.join(t))                 # Összerakja a str típusú (!!!) elemeket a delimiter mentén

    s3 = ' alma '
    print('->', s3.strip(), '<-', sep='')  # Leszedi a széléről a whitespace-ket. Rokonai: rstrip(), lstrip()


def comprehensionok_iteratorok():
    # Hasonlóan a matekos halmaz definíciókhoz: list/set/dict comprehension és generátor
    lc = [x * x for x in range(10) if x % 2 == 0]  # Az if opcionális és az x*x helyett bármilyen kifejezés lehet
    print(lc)
    # Ekvivalens forma, kevésbé idiomatikus:
    lc2 = []
    for x in range(10):
        if x % 2 == 0:
            lc2.append(x * x)

    sc = {x * x for x in range(10) if x % 2 == 0}
    print(sc)

    dc = {x: x * x for x in range(10) if x % 2 == 0}
    print(dc)

    g = (x * x for x in range(10) if x % 2 == 0)  # Ez más, mint a fentiek. Csak egyszer lehet végigmenni rajta
    print(g)

    # Ekvivalens forma
    def g2():
        for x in range(10):
            if x % 2 == 0:
                yield x * x  # Mint a return visszaadja az értéket, de nem lép ki a függvényből

    # Hívás:
    # g = g2()  # Példányosítás
    # for e in g:

    # Ez is generátor
    def g3():
        yield from range(10)  # Itt a paraméterként kapott iterárort nem egyben, hanem egyesével értékenként adja vissza

    for e in g:
        if e > 5:
            break
        print(e)

    print(next(g))  # Egyesével így lehet elfogyasztani

    # Nem reentráns! Ott folytatódik, ahol abbahagytuk
    for e in g:
        print(e)

    print(next(g, None))  # Ha nincs default érték adva, akkor exception-t dob


def halado_iteratorok():
    from itertools import repeat, cycle, islice, accumulate, batched, groupby
    from operator import mul

    # Az iterátorokon lehet értelmezni iterátorokat

    # Az enumerate sorszámot rendel az egyes elemekhez a start értéktől kezdődően
    # A zip pedig tuple-okat csinál az iterátorokból
    for n, (a, b) in enumerate(zip(range(10), range(10, 0, -1), strict=True), start=1):
        print(n, a, b)

    # Fun fact:
    z = zip(range(10), range(10, 0, -1))  # zip
    a, b = zip(*z)                        # unzip

    # Menetelés
    for e in islice(cycle(['bal', 'jobb']), 15):
        print(e)

    # Háromszoros hurrá az iterátoroknak!
    for e in islice(repeat(['Hip hip Hurrá!']), 3):
        print(e)

    # Aritmetikai összeg n=0-tól 19-ig
    a = accumulate(range(20))
    print(list(a))

    # n faktoriális n=0-tól 10-ig
    a = accumulate(range(11), mul)
    print(list(a))

    # Csoportokra osztás tetszőleges feltétel szerint csak rendezett adaton (mint az Unixos uniq parancs)
    def maradek_3(x):
        return x % 3

    from collections import defaultdict

    csoportok = defaultdict(list)
    for kulcs, csoport_iterator in groupby(range(20), key=maradek_3):
        csoportok[kulcs].append(list(csoport_iterator))

    for maradek, elemek in csoportok.items():
        print(maradek, elemek)

    # Hármas csoportokra osztás az egymást követő elemek csoportosításával
    a = batched(range(10), 3)
    print(list(a))

    # Külső library mégtöbb hasznos iterátorral
    # Pl. kiszámoló, kártyaosztás round robin módszerrel
    from more_itertools import distribute
    a = distribute(3, range(10))
    for e in a:
        print(list(e))


def lambda_fuggveny():
    # Általában a függvényenek van neve, de ha csak egy rövid függvényt szeretnénk, akkor nem kell nevesíteni
    def square(x):
        return x * x

    # lambda változat (mivel le van tárolva, ezért ugyanúgy van neve)
    square = lambda x: x * x

    print(square(5))  # 25

    # Ilyenkor nincs neve a függvénynek
    sorted(range(10), key=lambda x: -x)

    # Ilyen nincs. Nem lehet több statement egymás után
    # lambda x:
    #     y = x * 2
    #     return y

    r = (lambda x: x * 2)(10)  # Hívás név nélkül

    szorzas = lambda a, b: a * b  # Több paraméter

    hello = lambda name='Python': f'Hello, {name}!'  # Default érték is lehet

    elojel = lambda x: 'pos' if x > 0 else 'neg'  # Feltétel a lambdában

    x = 2
    x_elojele = 'pos' if x > 0 else 'neg'  # Így gyakrabban találkozhatunk a szerkezettel

    # Függvények, amik vonzzák a lambdát

    gen1 = map(lambda x: x * x, range(10))  # Idiomatikusan: (x * x for x in range(10))
    gen2 = filter(lambda x: x % 2 == 0, range(10))  # Idiomatikusan: (x for x in range(10) if x % 2 == 0)


def any_all_csillagok():
    # Említésre méltóak ezek a beépített függvények
    a = list(range(100))
    print(sum(a, start=0), min(a), max(a, default=0))  # Szokásos függvények. Opcionálisan az üres paraméter kezelhető

    print(any(x == 5 for x in range(10)), all(x > 0 for x in range(10)))

    # Az egy csillag
    numbers = [1, 2, 3]
    print(*numbers)  # A * "szétnyitja" az iterable elemeit ekvivalens ezzel: print(1, 2, 3)

    a, *b, c = list(range(10))  # Így is használható az elemek összegyűjtéséhez

    # Vagy szétszedéséhez
    a = (1, 2)
    b = (3, 4)

    r = (*a, *b)
    print(r)

    # Praktikusan változó számú argumentum esetén használjuk
    def atlag(*szamok):  # A paramétereket "összegyűjti" egy tuple-ba
        return sum(szamok) / len(szamok)

    atlag(1, 2, 3, 4)  # Ebben a jelölésben nem véletlenül hasonlítanak a paraméterek egy tuple-ra
    t = [1, 2, 3, 4]
    atlag(*t)  # Itt szétszedi tuple-ként, ha a bemenet halmaz volt, akkor változó sorrendben!

    # A két csillag ugyanez csak tuple helyett dict-tel
    default = {'szin': 'kek', 'meret': 10}

    overlay = {'meret': 20}

    r = {**default, **overlay}
    # v.ö.
    r2 = {*a, *b}

    # Praktikusan változó számú keyword argumentum esetén használjuk
    def fun(**a):  # A ** összegyűjti a dict tartalmát
        print(a)

    # fun(1, 2, 3)  # így nem fog működni, nincs nevük az értékeknek
    fun(a=1, b=2, c=3)  # Ezek igazából dict key value párok
    p = {'a': 1, 'b': 2, 'c': 3}
    fun(**p)

    # Különféle függvény szignatúrák csillagokkal
    def teljesen_hatarozatlan(*args, **kwargs):  # Az args és kwargs nevek csak konvenció
        print('args:', args)
        print('kwargs:', kwargs)

    teljesen_hatarozatlan(1, 2, 3, verbose=True, repeat=30)

    def create_user(name, *, age, city):  # A * után csak kewyord argument lehet
        print(name, age, city)

    def example(a, b, /, c, d):  # A / előtt csak sima pozícionális argumentum lehet
        print(a, b, c, d)

    # Argumentumok továbbadása
    def belso(a, b):
        pass

    def kulso(**kwargs):  # Ez összeszedi
        belso(**kwargs)   # Ez szétszedi

    def kulso2(*args):  # Ez összeszedi
        belso(*args)    # Ez szétszedi

    def kulso3(*args, **kwargs):  # Egyszerre a kettőt összeszedi
        belso(*args, **kwargs)    # Egyszerre a kettőt szétszedi


if __name__ == '__main__':
    prefixalt_stringek()
    alap_string_muveletek()
    comprehensionok_iteratorok()
    halado_iteratorok()
    lambda_fuggveny()
    any_all_csillagok()
