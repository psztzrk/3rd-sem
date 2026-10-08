def fuggvenyek():
    def fun():  # A függvény definíciója. A külső scope-ban van definiálva (általában a globális) és egyszer fut le
        print('valami')  # A függvény belseje, indentálva van, minden hívásnál lefut

    fun()  # A függvény hívása a neve utáni zárójelekkel. A függvény nevére ugyanaz vonatkozik, mint a változókra

    fun.__call__()  # A () eyecandy a függvény objektum rejtett függvényéhez (Lásd később objektumok)

    def fun2(b, c, d=2):  # Paraméterek sorban változónévvel jelölve. Opcionálisan default értékkel
        print(b, c, d)

    # def fun3(b=3, c):  # A default értékes paraméter után nem lehet olyan, aminek nincs default értéke
    #     print(b, c)

    def fun3(b=3, verbose=None):  # Ilyenkor None-t szokás írni, hogy szintaktikailag helyes legyen
        print(b, verbose)

    fun2(1, 2, 3)  # A default érték felülírható
    fun2(1, 2)     # vagy elhagyható

    fun3(verbose=2, b=4)  # Ha névszerint adjuk meg az paraméterértékeket híváskor, akkor tetszőleges sorrend lehetséges

    fun3(3, verbose=True)  # A két fajta paraméter megadás keverhető, amíg a sorrendit követi a név szerinti
                           # A névszerinti praktikus a literális paraméter érték megadáskor, magyarázatnak

    # Vissaztérési érték
    def fun4():
        print('Ez a függvény None-t fog visszatéríteni')
        # Ha nincs semmi implicit None-t jelent

    print('None a visszatérési érték:', fun4())

    def fun5():
        return  # Ez is None-t térít vissza

    def fun6():
        return None  # Meg ez is

    def fun7():
        return 'valami', 'valami', fun6()  # Itt bármilyen kifejezés lehet, ami lehet jobboldal

    def dokuemntalt_fuggveny():
        """ Amit ide írunk többsoros string formában az lesz a docsstring"""

    print('Speciális helyre kerül:', dokuemntalt_fuggveny.__doc__)

    # Így láthatjuk viszont
    print(help(dokuemntalt_fuggveny))


def global_demo():
    global global_var  # Ha ezt kikommentáljuk, akkor a global_var a global scopeban nem változik
    global_var = 'módosított globális'  # global kulcsszóval a globális scope-ban változtatja az értéket


def nonlocal_demo():
    x = 'szülő érték'

    def belso_fuggveny():
        nonlocal x  # A kulso_fuggveny x-ét fogjuk módosítani enélkül csak sima lokális változó lesz
        x = 'új belső érték'

    belso_fuggveny()
    print('Külső x:', x)  # Ha van nonlocal, akkor a belső függvény módosítását látjuk. Ha nincs, az eredeti értéket


def minden_fuggveny_felulirhato():
    global int     # Ez azért kell, mert az int globálisan definiált függvény. Global scopeban nem kell
    old_int = int  # Zárójelek nélkül, csak a definiált objektumot írjuk le, nem történik függvényhívás
    int = float    # Minden objektumhoz definiálható () operátor, minden objektum felülírható
    print('Float:', int('6'), 'Int:', old_int('5'))
    int = old_int
    # None = True  # A kulcsszavaknál ez nem működik


def import_es_print_fuggveny():
    import sys                         # Sima import, teljes modult importál. Ilyenkor sys.stderr-al hívjuk a tartalmát
    from sys import stderr             # Lehet csak bizonyos függvényeket importálni
    from sys import stdout as kimenet  # Az as kulcsszóval át lehet nevezni az importált dolgot (modult is)

    print('Több', '(típusú)', 'paraméter is lehet:', 19, 20.0 - 1, True, None)  # Implicit str()-el
    print('A paraméter elválasztó és a vég állítható:', sep=' ', end='\n')  # Alapból space és újsor
    print('valami', 'valami2', 13, 343, sep='\t')  # Tab Separated Values (TSV)...
    print('valami', 'valami2', 13, 343, sep=',')  # Comma Separated Values (CSV)...

    print('Initialising...', end='')  # Egy sorban meg lehet várni egy eredményt
    import time
    time.sleep(1)
    print('Done')

    # Alapvetően a stdout-ra ír, de felül lehet bírálni. Akár fájlba is írhatunk!
    # A flush=True azonnal kiírja a paramétereket. Alapból az OS-re bízza
    # pl. Ha átirányítjuk a kimenetet, akkor a végén ír ki mindent
    # -> A PYTHONUNBUFFERED=1 környezeti változó megadása esetén ekkor is egyből kiír mindent
    print(1, file=sys.stderr, flush=True)


def type_es_id():
    print(type('string'), type(1), type(2.0), type(None), type(True))  # Kiírja a típust
    print(isinstance(1, int))  # Így teszteljük a típust
    print(id(1), id('string'), id(2.0))  # Az objektumok azonosítója. id nevű változót ne akarjunk, foglalt!


def range_tipus():
    # Mint az Unix shell seq parancsa
    start = 0  # A Python 0-tól indexel
    stop = 10  # A véget nekünk kell megadni mindig
    step = 1  # A default lépésköz 1
    r = range(stop)
    r2 = range(start, stop)
    r3 = range(start, stop, step)

    print('Így lehet range-t definiálni:', r, r2, r3)

    print(3 in r3)  # Tartalmazást lehet nézni benne. Balról zárt, jobbról nyílt a definiált intervallum
    print(3 not in r3, not 3 in r3)  # Mindkettő formátum jó a negálásra. Az első konvencionális, mert természetesebb

    r4 = range(10, 1, -2)  # A negatív indexek is támogatottak, ha van értelmük (a start-stopot meg kell fordítani)
    print(r4.start, r4.stop, r4.step)  # A paraméterek read-only attributeként lekérdezhetők
    # r4.stop = 11  # Ez hibát ad

    print(list(range(10)))  # Például így kiteríthető az intervallum


def egyszeru_loopok():
    e = 0  # Arra az esetre, ha a ciklusból egy kör se fut le
    for e in range(10):
        print(e)

    print(e)  # A ciklusváltozó elérhető marad, feltéve ha legalább egy kört futott a ciklus (nem üres az iterátor)

    for e in range(10):
        print(e)
        if e > 2:
            if e == 5:
                break  # Kilép a ciklusból
            else:
                continue  # Kilép a ciklus aktuális köréből
        print('valami')
    else:  # Csak akkor fut le, ha ciklus nem lehet megszakítva (break által)
        print('ez a for else ága')

    e = 0
    while e < 10:
        e += 1
        if e == 5:
            break  # Kilép a ciklusból
        else:
            continue  # Kilép a ciklus aktuális köréből
    else:
        print('A While else ága')

    # Nincs hátultesztelős ciklus
    # do:
    #    print('valami)
    # while BOOLEAN_CONTEXT


def tuple_list_set_frozenset():
    # Heterogén típusokat is lehet tárolni az alábbi konténerekben akár rekurzívan is, tetszőleges mélységben:
    t = ('1', 2, 3.0, 4)  # () tuple() tuple([1, 2, 3, 5]) Immutable
    l = ['1', 2, 3.0, t]  # [] list()  list([1, 2, 3, 4])  Mutable
    s = {'1', 2, 3.0, t}  # _  set()   set([1, 2, 3, 4])   Mutable, csak immutable elemeket tartalmazhat, nincs sorrend!
    f = frozenset(s)      # _  frozenset()                 Immutable, a set immutable párja, mint a listnek a tuple

    print(t, l, s)
    l.append(True)    # Egy "True" elem hozzáadása a végére. Ebből tudjuk, hogy list()
    s.add(False)      # Egy "False" elem hozzáadása. Ebből tudjuk, hogy set()
    # t.append(True)  # Ez nem létezik
    # t.add()         # Ez nem létezik
    l.extend([1, 2])  # Lista hozzafűzése a lista végéhez
    s.update({1, 2})  # Halmaz hozzafűzése a halmazhoz
    print(l, s)
    l.insert(0, None)  # Ez az első paraméternek megfelelő indexbe rakja az új elemet
    print(l)
    l.pop(2)       # A megadott indexen lévő elemet kiszedi a listából és visszaadja
    l.remove(3.0)  # Érték alapján szed ki elemet a listából, nem adja vissza. ValueError-t dob ha nincs ilyen elem
    s.pop()        # Visszaad egy elemet a halmazból. Nincs paramétere
    print(l, s)

    l2 = [1, 2, 3]
    s2 = {1, 2, 3}
    l2.clear()  # Törli a listából az elemeket  vs. l2 = [] ami új listát hoz létre
    s2.clear()  # Törli a halmazból az elemeket vs. s2 = set() ami új halmazt hoz létre
    print(l2, s2)

    print(2 in t)  # Lineáris keresés O(n)
    print(2 in l)  # Lineáris keresés O(n)
    print(2 in s)  # Hash alapú keresés O(1)

    # Formátumbeli alternatívák (mindháromra működik, sőt továbbiakra analóg módon)
    g = (1, 2, 3,)  # Ez OK
    h = (  # Ez a forma lehetővé teszi, hogy a sor alapú verziókezelők diffje csak a lényeget mutatja
        1,
        2,
        3,
    )

    a, b = 1, 2      # Ennek az ekvivalens alakja:
    (a, b) = (1, 2)  # Mert hogy tuple-t adunk értékül egy másiknak csak kicsomagoljuk az elemeit
                     # Konvenció: Ahol lehet, a zárójelet elhagyjuk

    print(len(l))  # A konténer elemszáma

    # Halamazműveletek
    s = {1, 2, 3}
    s2 = {2, 3, 4}

    print('Unió:', s | s2, s.union(s2))  # s |= s2 vagy s.update(s2)
    print('Metszet:', s & s2, s.intersection(s2))  # s &= s2 vagy s.intersection_update(s2)
    print('Különbség:', s - s2, s.difference(s2))  # s -= s2 vagy s.difference_update(s2)
    # s ^= s2 vagy s.symmetric_difference_update(s2)
    print('Szimmetrikus különbség:', s ^ s2, s.symmetric_difference(s2))

    # A metódusoknál elég, hogy az első elem legyen halmaz a második elég ha iterálható
    # Az operátoroknál by design halmaz kell
    print('Unió:', s.union(l))
    # ...

    print(s.isdisjoint(s2), s.issubset(s2), s.issuperset(s2))  # Halmaz vizsgálatok


def lista_tuple_indexeles_rendezes():
    l = [1, 2, 3.0, 4]
    l2 = [l, [], 2, 3]

    # Az indexelés a list() és tuple() esetén hasonlóan működik mint a range(). slice()-nak hívják
    # A set() értelemszerűen nem indexelhető
    print(l[0])            # Valahányadik elem. Az értéke mehet 0-tól len(l) -1 ig
    print(l2[0][2])        # Beágyazott listák indexelése
    # print(l[342]         # Túlindexelés. Exceptiont fog dobni
    # print(l.index(342))  # Túlindexelés. Exceptiont fog dobni
    print(l[0:])           # Valahányadiktől végig egy új lista
    print(l[342:])         # Új üres lista. Sosincs túlindexelés slice esetén
    print(l[:-1])          # Az első elemtől az utolsó előtti elemig egy új lista
    print(l[1:-1:2])       # A második elemtől az utolsó előtti elemig kettesével egy új lista
    print(l[None:-1])      # Az üres helyekre None is írható. Ugyanazt jelenti, mintha nem írnánk semmit

    # print(l[342]   # Túlindexelés
    # print(l.index(342))  # Exceptiont fog dobni

    # A slice-olásnál

    print(l[::-1])  # Ez vajon mit csinál?
    l3 = l[:]       # és ez?
    l3.append('alma')
    print(l, l3)

    l.reverse()  # Helyben módosítja a listát
    print(l)
    print(list(reversed(l)))  # Csinál egy view-t, amin végig lehet menni, indexelni, stb. vagy új listát csinálni
    l.sort()  # Helyben rendezi a listát
    print(sorted(l))  # Csinál egy másolatot a listáról, ami rendezett lesz

    def key_fun(x):
        return -x

    # Opcinális rendezési kulcs megadható, illetve a rendezési sorrend is növekvőről csökkenőre állítható
    sorted(l, key=key_fun, reverse=True)


def dict_defaultdict_counter():
    s = {1, 2, 3, 4}  # _  set()   set([1, 2, 3, 4])      Mutable, csak immutable elemeket tartalmazhat, nincs sorrend!
    d = {1: 2, 3: 4}  # {} dict()  dict([(1, 2), (3, 4)]) Mutable, csak immutable elemeket tartalmazhat, VAN sorrend!
    # A dict() egy betűvel hosszabb, így ő lett a {}. A value-ra nincs megkötés csak a key-re
    # A dict() insertion orderben van a Python 3.7 óta. Tetszőleges keyt alkalmazva használható rendezet halmazként

    print(d[1])      # Elem lookup
    d[12] = 32       # Értékadás
    print(d[12])
    d[1] = 32        # Elem felülírása
    # print(d[32])   # Nem létező key, Exception: KeyError
    print(d.get(1))  # Nem létező key esetén None-t ad vissza. A második paraméterben a None felülírható

    print(d.keys(), d.values(), d.items())  # Különféle view-ek, amik támogatják a halmazműveleteket
    print(d.keys().isdisjoint({1, 2, 3}))
    print(2 in d)  # A kulcsok között néz tartalmazást

    # Tipikus pattern: Egy gyakorisági eloszlás meghatározása
    for e in range(10):
        if e in d:  # Mivel eleinte nincs benne a kulcs, KeyErrort adna, kell az if
            d[e] += 1
        else:
            d[e] = 1

    from collections import defaultdict, Counter
    d2 = defaultdict(int)  # Default factory: int() -> 0

    # Egy gyakorisági eloszlás meghatározása
    for e in range(10):
        d2[e] += 1  # Itt nem kell az if, ha nem létezik a key, lefut a default factory

    # Gyakori felhasználási forma pl. osztályozáshoz
    d3 = defaultdict(list)
    d4 = defaultdict(set)

    for e in range(10):
        d3[e % 2].append(e)  # Az egyes előfordulásokat tartjuk nyilván
        d4[e % 2].add(e)     # A különböző elemeket tartjuk nyilván

    # Mély defaultdict:
    # Ilyen nincs: d2 = defaultdict(defaultdict(set)) # defaultdict(set)()
    # Helyette:
    def f():
        return defaultdict(set)

    d5 = defaultdict(f)

    c = Counter()  # -> defaultdict(int) + extrák meg gyorsabb is

    c = Counter('aafsfsdbbbaaaa')  # Gyakoriságot számol elemenként
    print(c)
    print(c.most_common(23))  # Kiírja a TOP 23 elemet c.most_common() az összeset gyakorisági sorba rendezve

    for x in d:  # Ekvivalens: d.keys()
        print(x)

    for k, v in d.items():
        print(k)
        print(v)




if __name__ == '__main__':
    fuggvenyek()

    global_var = 42
    global_demo()
    print('global_var:', global_var)

    x = 'Global x'
    nonlocal_demo()
    print('Global x nem változik:', x)

    minden_fuggveny_felulirhato()
    import_es_print_fuggveny()
    type_es_id()
    range_tipus()
    egyszeru_loopok()
    tuple_list_set_frozenset()
    lista_tuple_indexeles_rendezes()
    dict_defaultdict_counter()
