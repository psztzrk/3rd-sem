def stringe_jelolesek():
    # Mindkét határoló megengedett szemben pl a C/C++-al
    # Konvencionálisan egyet (" a standard) érdemes konzisztensen használni
    s = 'Ez egy string'
    s2 = "Ez is egy string"

    # De csak egy sorban, ha sortörést akarunk, akkor a sor utolsó karaktere (!) visszaper kell, hogy legyen
    s3 = "Ez is egy \
           string sok space-szel a közepén, egy sorban."
    print(s3)

    # Szebben néz ki a kódban (nincs extra space az elején "a második sornak") cserébe zárójelekkel határoljuk
    s4 = ("Ez egy"
          " string")
    print(s4)

    # Ez egy többsoros string
    s5 = """Ez is egy
    string.
            Többsoros is lehet. Kiíráskor megmaradnak a sortörések."""

    print(s5)

    s5 = '''Ez a párja az előzőnek.
            Létezik, de konvencionálisan nem használjuk.'''
    print(s5)

    # Literális macsakakörmök és aposztrófok

    s6 = "Ez is 'egy' string"
    print(s6)

    s7 = 'Ez az elző string "párja" '
    print(s7)

    s8 = "Ezek az escape-k: \\ \" ' egy stringben"
    print(s8)

    s9 = 'Ezek az escape-k: \\ \' " egy stringben'
    print(s9)

    s10 = """Ezek az escape-k: \\ ' " \""" egy stringben"""
    print(s10)

    s10 = '''Ezek az escape-k: \\ ' " \''' egy stringben'''
    print(s10)

    # Ez a string konstruktora. Pl ha szám típusból kell stringet csinálni
    s11 = str(123)
    s12 = str()
    print(s11, 'az str() üres string:', s12)

    print('a' + 'b')  # Konkatenáció, új stringet csinál. Az s += 'alma' nem létezik, csak új string hozható létre

    print('=' * 80)  # Sorminta

    print(len(s11))  # A string hossza karakterben

    s13 = 'string'
    print('str' in s13)  # Tartalmazás operátor (lineáris keresés)


def kommentek_jelolese():
    print('ez kód')  # Ez egy komment, ami csak egysoros lehet
    # a folytatás a második sorban ugyanúgy prefixáladó
    # Minden ami a # -után jön a sor végéig komment. Konvenció: 2 space a kód után és egy space a # -után

    # Többsoros komment

    """
    Ez egy több 
    soros komment

    Valójában egy string a fenti formátumban, ami nincs semminek értékül adva
    """


def valtozonevek_jelolese():
    valtozo = 'Ez egy érték'  # Kisbetűvel

    ez_egy_valtozo = 'érték'  # esetleg snake case-szel

    cammelCaseValtozo = 3.14  # Ezt is "lehet", de nem szép, mert a cammel case másra van "fenntartva"

    KONSTANS = 3.14  # A global scopeban a fájl elején az importok után

    print(KONSTANS)
    KONSTANS = 2.71  # Semmi sem akadályozza meg, hogy megváltozzon. Ez valójában egy sima változó nem sima névvel
    print(KONSTANS)

    class EzEgyClass:  # A classok neve Nagybetűvel cammel case-szel írandó a konvenció szerint
        pass

    árvíztűrőtükörfúrógép = 43  # Működik (szinte bármilyen UTF-8 karakter jó), nem konvencionális, IDE nem szereti

    az_elet_ertelme = 42  # A változónaevek lehetnek hosszúak, magyarázóak
    # -> A komment el tud mászni a kód mellől, de a változónevek nem

    # 1valtozo = 19  # Számmal nem kezdődhet a változónév! Ha ez nem komment, nem fut le a kód. Ki lehet próbálni!


def ertekadasok_es_egyenlosek_vizsgalat():
    bal_oldal = 'jobb_oldal'  # Az egyenlőségjel körül (és amúgy az operátorok körül) space-t konvencionális írni

    valami = 'komplex_kifejezés'  # Kiértékeli a jobboldalt és az eredmény pointerjét adja a baloldali címkének (!)
    # Olcsó művelet -> Selfdocumenting code, nincs túlindexelés vö. C/C++
    # char[4] = "Hello!"; // Ez túl lett indexelve, a compiler szól érte

    # 'jobb_oldal' = bal_oldal  # Nem felserélhető a két oldal a működésből adódóan

    'alma' == 'körte'  # Ez nem értékadás, hanem egyelőségvizsgálat, ez OK

    'alma' != 'körte'  # Ez az egyelőségvizsgálat negált párja

    # 'alma' === 'körte'  # A Javascriptnél van, itt nincs. A típusellenőrzés az adott osztály dolga (lásd később)

    # b = n := 2  # Ilyen nincs
    b = (n := 2)  # De ilyen van. Ez a warlus operator. Gyakorlatilag értékadás + a jobboldal továbbadás egyszerre
    if (n := len('string')) > 10:  # Tipikus használati eset
        print('Túl hosszú a string:', n, 'elem')

    bal_oldal = 'alma' == 'körte'  # Ez is OK, mert a jobboldal egy kifejezés

    x = 'alma' == 'körte' == 'dinnye'  # Láncolt egyelőség vizsgálat. Ilyenkor mindhárom tényező egyenlő kell legyen

    x = y = 'z'  # Láncolt értékadás. Ilyenkor x és y értéke is 'z' lesz

    x, y = 1, 2  # Szimultán értékadás. Egyszerre, atomi módon történik
                 # C-ben nincs ilyen C++ nyelvben a C++11 és C++17 nyelvi verziók körül jelent meg

    x, y, z = y, x, 3  # Akár röptében is cserélhetők a változók (akárhány elem)


def osszehasonlitasok():
    x, y = 'a', 'b'  # Létezik stringek között rendezés. A lexikografikus rendezés szabályai szerint

    x < y
    x > y
    x == y
    x >= y
    x <= y
    # x => 2  # Tehát ilyen nincs
    # x =< 2  # És ilyen sem

    z = 1
    0 <= z <= 10  # Viszont ilyen van
    x = z <= 2    # És ilyen is


def booleanok_es_none():
    True  # Kulcsszó. Nagybetűvel. Statikusan létező érték. True ~ nem 0, nem üres string, stb.
    False  # False ~ 0, üres string, stb.

    false = True  # Lehet ilyet csinálni, de a kisbeűs már sima változó (pl. a Javascriptben kisbetűs a true/false)
    true = False

    None  # Extremális elem. Kulcsszó, ezért statikusan létezik. Semmivel sem egyelő, kivéve saját magával

    x = True
    x is None  # A konvenció szerint így teszteljük a None értéket. Gyorsabb, közvetlenebb, nem átírható tesztelés
    x == None  # Ez felüldefiniálható, érték szerint tesztel nem azonosságot, átírható (lásd objektumok)

    # Mit írnak ki ezek a booleanra való castolások?

    a = bool(1)
    b = bool(0)
    c = bool('')
    d = bool('valami')
    e = bool('False')
    f = bool(None)
    g = bool('None')
    h = bool()

    print(a, b, c, d, e, f, g, h)


def int_es_float():
    i, f = 1, 1.0  # Int: sima szám. Float: tizedes pontot tartalmazó szám. Mindkettő tetszőleges pontosságú objektum(!)

    i2, f2 = 100_000_000_000_000, 100_000_000_000_000.123  # Snake case is használható az olvashatóság miatt
    i3, f3 = 1e15, 1.123e15  # Exponenciális jelölés is használható
    f4 = .2  # 0.2 rövid jelölése

    print(int('1'), float('1.0'))  # A konstruktorok alapból 10 es számrendszerben
    print(int('FF', base=16), int('10', 2))  # Második paraméterként lehet számrendszert megadni
    print(int('0x10', 0))  # Vagy prefixum alapján dönti el a számrendszert
    print(int(3.2))  # Csonkolva lesz az egész értékre
    print(float('3'))  # Az ekvivalens float értéket kapja meg
    print(float(True), int(False))  # 1.0 és 0
    print(float('inf'), float('-inf'), float('nan'))  # inf mindennél nagyobb, -inf kisebb, nan semmivel sem egyelő
    # int('harom')  # Ilyen nincs
    # float('harom')  # Ilyen sincs

    1 == 1.0  # Érték szerint a két típus szokásos műveletei kompatibilisek

    # '1' < 2  # Ilyen nincs
    # x = 2 + 'harom'  # Ilyen sincs

    f = 10
    i = 2
    print('Floattá konvertálódik:', f + i, i - f, i * f, f / i)
    print('Egészosztás és maradék, int lesz az eredmény:', f // i, f % i)

    # Az augmented assignmentek léteznek
    i += 1  # Ekvivalens: i = i + 1 De nem létezik ++i és i++
    # ...


def if_szerkezet():
    BOOLEAN_CONTEXT = 2 < 3
    if BOOLEAN_CONTEXT:  # Az if és a : között bármiből Bool lesz implicit módon
        print('A feltétel teljesült')  # Indetálni kell az if ágait min 1 space lehet tab is, 4 space a konvenció

    if BOOLEAN_CONTEXT:
        print('A feltétel teljesült')
    else:  # Opcionális else ág, ha nem teljesül a feltétel
        print('A feltétel nem teljesült')

    if BOOLEAN_CONTEXT:
        print('A feltétel teljesült')
    elif 'Ez is boolean context, mivel nem üres a sting mindig True lesz':
        print('"A második if feltétel teljesült" ág')
    else:  # Opcionális else ág, ha nem teljesül a feltétel
        print('Egyik feltétel sem teljesült')


if __name__ == '__main__':
    stringe_jelolesek()
    kommentek_jelolese()
    valtozonevek_jelolese()
    ertekadasok_es_egyenlosek_vizsgalat()
    osszehasonlitasok()
    booleanok_es_none()
    int_es_float()
    if_szerkezet()
