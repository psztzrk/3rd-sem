def exceptionok():
    myints = []
    try:
        # Legszűkebb kritikus kód. Itt nyilvántart mindent az esetleges rollback miatt -> lassabb, bármi hibázhat
        myints[2] = int('három')  # Ez ValueError (jobb oldal) aztán ha eljutna a bal oldalig IndexError
        myints['alma'] / 0  # TypeError aztán ZeroDevision error lenne ha eljutna odáig
    except (KeyError, NotImplementedError):  # Vagylagosan több is összefogható
        pass  # Ignore. Ilyenkor pl. hiányozni fog a változó, amit nem sikerült inicializálni
    except IndexError as e:
        # Lehet továbbmenni ha csak értéket adunk, printelünk, stb.
        myint = 3
        # Lehet a kapott hibával valamit kezdeni
        print('Hiba volt:', e)
        raise  # Újra raiseli az exceptiont ha előtte megcsináltuk, amit akartunk
    except TypeError as e:
        msg = str(e)
        raise AttributeError('Új üzenet. Utána a régi:', msg) from e  # Ilyenkor láncolódik az új exception az e-re
    except ZeroDivisionError:
        raise ValueError('Új üzenet') from None  # Az eredeti hiba el van rejtve
    except Exception as e:  # Univerzális exception, ugyanúgy mint az "except:" catch-all-ként működik
        print('Na, ezt nem láttam jöni:', e)
    else:  # Ez csak az exceptek után jöhet, ha vannak
        print('Huh! Nem volt hiba')
    finally:  # Ez csak a legvégére mehet, bármi is van előtte
        # Itt kell felszabadítani a resource-okat, akárhogy is végződik a kaland -> Szeparálva van a többi logikától
        print('Akárhogy is volt, én lefutok')

    # A pontos exception nevek a dokumentációban teljeskörüen olvashatók, vagy ki lehet próbálni mit ad hiba esetén
    class SajatException(Exception):
        """Mert van egy eddig ismeretlen jó okunk hogy hibáztassunk valakit"""
        pass

    try:
        raise SajatException('Saját üzenet')
    except SajatException as e:
        print('Hiba történt:', e)


def path_kezeles():
    # Az os és os.path régi és kényelmetlen modulok, a modern pathlib javasolt. Néha rá kell szólni az LLM-re
    from pathlib import Path

    # Aktuális mappa (Current Working Directory)
    mostani_mappa = Path.cwd()
    print(__file__)

    # Felhasználó saját mappája (Home directory: pl. C:\Users\Nev vagy /home/nev)
    home_mappa = Path.home()

    # Útvonalak összefűzése a PER ( / ) operátorral!
    # Nem kell többé os.path.join-t használni, a Python elintézi a \ és / jeleket automatikusan
    # Jegyzet: Az '/'.join() és '\\'.join() platformfüggő, az os.path.join() a megfelelőt használta
    fajl_utvonal = home_mappa / 'Dokumentumok' / 'projekt' / 'adatok.txt'

    # Unix formátumúra konvertálja a Path-t
    fajl_utvonal.as_posix()

    utvonal = Path('/home/user/Dokumentumok/jelentese_2026.v2.txt.gz')
    print(utvonal.name)         # 'jelentese_2026.v2.txt.gz' (A teljes fájlnév)
    print(utvonal.stem)         # 'jelentese_2026.v2.txt'    (A fájlnév a legutolsó (!) kiterjesztés nélkül)
    print(utvonal.suffix)       # '.gz'                      (A legutolsó kiterjesztés)
    print(utvonal.suffixes)     # ['.v2', '.txt', '.gz']     (Az összes kiterjesztés listája)
    print(utvonal.parent)       # '/home/user/Dokumentumok'  (A szülőmappa, mint a .parents[0])
    print(utvonal.parents[2])   # '/home'                    (A szülőmappa kettővel följebb, a harmadik)
    print(utvonal.parts)        # ('/', 'home', 'user', 'Dokumentumok', 'jelentese_2026.v2.txt.gz')
    print(utvonal.parent.name)  # Láncolhatók a tulajdonságok

    p = Path.cwd()  # Path('adatok.txt')

    print(p.exists())       # True, ha létezik (mindegy, hogy fájl vagy mappa)
    print(p.is_file())      # True, ha létezik ÉS fájl
    print(p.is_dir())       # True, ha létezik ÉS mappa

    # Metaadatok lekérése
    info = p.stat()
    print(info.st_size)     # Fájlméret bájtokban
    print(info.st_mtime)    # Utolsó módosítás időbélyege (timestamp)

    mappa = Path.cwd()

    # Csak a mappa közvetlen tartalmának listázása a glob kifejezések nem regexek!
    for elem in mappa.glob('*'):
        print(elem.name)

    # Az összes .py kiterjesztésű fájl megkeresése a mappában és az almappákban is
    for python_fajl in mappa.rglob('*.py'):  # Ugyanaz, mint a glob('**/*.py')
        print(python_fajl)


def fajl_io():
    # STDINről olvas enterig vár vagy ctrl-D (Linux) ctrl-Z + enter (Windows)
    name_str = input('My name is ')
    num_str = input('My name favorite number is ')  # Ha számot kérünk be, az is string. Manuálisan konvertálandó!

    # Az open() default módja az 'r', a system encoding (=az alaprendszer szerint változhat, Dockerben ált. C ~ ASCII)
    # és az universal newlines. Ezek elhagyhatóak
    # Érdemes az encodingot mindig explicit megadni UTF-8-nak, a mode-t akkor ha nem 'r' a többi jó defaulton
    # Path()-t is elfogad fájlnévként, nem csak str-t vagy bytes-t
    fhs = open('valami_str.txt', 'w', encoding='UTF-8')  # File handle, str jön belőle
    fhb = open('valami_bytes.txt', 'wb')  # Bytes jön belőle, nincs soha encoding paraméter

    # Fájlba írás csak azt írja bele, amit explicit megadunk
    fhs.write('valami')
    fhs.writelines(['line1', 'line2'])  # Bármilyen iterálhatót elfogad
    print('ezt printeljük', file=fhs)  # Ez úgy működik mint a print(), csak fájlba. Alapból rak újsort. Ez javasolt

    # Figyelni kell, hogy a file handlenek megfelelő típust adjunk át, mert csak az jó!
    fhb.write(b'valami')
    fhb.writelines([b'line1', b'line2'])

    # Itt sok dolog van, általában elfelejti az ember lezárni a fájlt, aztán a GC vagy takarít vagy nem
    # Ilyenkor elfogyhat a descriptor, amit az OS kezel. Ez a klasszikus nyelvek gondja, Pythonban erre ott a with
    fhs.close()
    fhb.close()

    # A with kulcsszó, másnéven context manager egy Python idióma
    # Csinál egy scope-ot ("contextet") a megnyitott fájlnak. Ha vége a scope-nak implicit bezárja a fájlt
    with open('valami_str.txt', encoding='UTF-8') as fhs:
        content = fhs.read()               # Paraméter nélkül az egész fájlt egybe beolvassa. Nem javasolt
        content = fhs.readline()           # Egy sort olvas be
        content = fhs.readlines()          # Az összes sort listában olvassa be, rajta hagyja az újsort a sorok végén
        content = fhs.read().splitlines()  # Ugyanaz, mint a readlines() csak leszedi az sorvég karakterket
        # Javasolt recept: soronként olvas be, nagy fájlokra is működik
        for line in fhs:
            # Universal newlines: Minden Unix newline-ra (\n) van konvertálva automatikusan bemenetnél
            # és az OS defaultra (!) kimenetnél (Windowson \r\n Linuxon \n) a Pythonon belül minden \n ként kezelendő!
            # Manuális newlines (reproducibility): open('valami_str.txt', 'w', encoding='UTF-8', newline='')
            line = line.rstrip()
            print(line)

    # Minden is fájl a 80-as évek óta (Unix)
    import bz2

    with bz2.open('valami.txt.bz2', 'wt', encoding='UTF-8') as fh:
        pass

    import gzip

    with gzip.open('valami.txt.gz', 'wt', encoding='UTF-8') as fh:
        pass

    from zipfile import ZipFile

    with ZipFile('valami.zip', 'w') as myzip:
        # Ez ugye több fájlt is tartalmazhat, bonyolultabb. Lezáráskor írja a TOC-ot a fájlba, különben korrupt lesz
        # A régi zip fájlok olvasásához ott a "metadata_encoding" hogy az ékezetes path-ok dekódolódjanak
        pass

    from urllib.request import urlopen

    with urlopen('https://google.com') as response:
        # Beolvassuk a teljes weboldal tartalmát (nyers bájtokként)
        weboldal_adat_bytesban = response.read()

    from multiprocessing import Pool

    with Pool(5) as p:  # CPU bound párhuzamosítás, nagy batchekkel mert mozgani kell az adatot a processek között
        pass  # result = p.map(fun, data)

    from concurrent.futures import ThreadPoolExecutor

    with ThreadPoolExecutor(max_workers=3) as executor:  # I/O bound párhuzamosítás, egy processen belül nagy I/O waitre
        pass  # executor.map(fun, data)

    # (SQL) adatbázis kapcsolat (tranzakció), saját (de)cipher, stb.

    # Saját contextmanager

    from contextlib import contextmanager
    from pathlib import Path

    @contextmanager  # Decorator, később az OOP-nél
    def file_logger(path: Path):
        # Ez történik a with-nél
        path.parent.mkdir(parents=True, exist_ok=True)
        f = path.open('a', encoding='UTF-8')
        try:
            yield f  # Ezt adja vissza az as
        finally:
            f.close()  # A végén e felejtsük el bezárni, bármi is történjék

    # Használat
    with file_logger(Path('valami.txt')) as logger:
        pass


def timeit_hasznalat():
    import timeit

    # Ez egyszer fut le
    setup = """
data = list(range(10_000))
data_set = set(data)
    """

    # Az első paraméter number alkalommal fog lefutni
    list_time = timeit.timeit('9999 in data', setup=setup, number=100_000)
    set_time = timeit.timeit('9999 in data_set', setup=setup, number=100_000)

    # Az össz futás ideje a number futtatásnak a setup nélkül
    print(list_time)
    print(set_time)

    # Többször futtatja a mérést, hogy átlagolni lehessen. 1 setup, 10_000 futtatás/kör, 5 kör
    list_times = timeit.repeat("9999 in data", setup=setup, number=10_000, repeat=5)
    set_times = timeit.repeat("9999 in data_set", setup=setup, number=10_000, repeat=5)

    print('list', f'{sum(list_times) / len(list_times):.10f}', '(' + ', '.join(f'{r:.10f}' for r in list_times) + ')')
    print('set ', f'{sum(set_times) / len(set_times):.10f}', '(' + ', '.join(f'{r:.10f}' for r in set_times) + ')')


def ngram_generator():
    import timeit
    from itertools import islice, tee

    # Az n-grammok átlapolódó egymás után következő fix hosszú karaktersorozatok. Hogy gyorsabb legenerálni őket?

    # Sliceolás
    def ng_index(inp, n):
        inp = list(inp)

        for i in range(len(inp) - n + 1):
            yield ''.join(inp[i:i + n])

    # Iterátorok
    def ng_iter(inp, n):
        for ngram in zip(*(islice(it, i, None) for i, it in enumerate(tee(inp, n)))):
            yield ''.join(ngram)

    def consume(iterator):
        for _ in iterator:
            pass

    inp_data = str(list(range(1_000_000)))
    n_len = 5

    index_time = timeit.repeat(lambda: consume(ng_index(inp_data, n_len)), number=1, repeat=3)
    iter_time = timeit.repeat(lambda: consume(ng_iter(inp_data, n_len)), number=1, repeat=3)

    print('index', f'{sum(index_time) / len(index_time):.10f}', '(' + ', '.join(f'{r:.10f}' for r in index_time) + ')')
    print('iter ', f'{sum(iter_time) / len(iter_time):.10f}', '(' + ', '.join(f'{r:.10f}' for r in iter_time) + ')')


def meres2():
    """Melyik optimalizált módszer jobb? find(), n-gram iterátor, regex (a boilerplate LLM-ből van, nem fontos) """
    # Megjegyzés: 3 percig fut kb, előre érdemes elindítani
    import re
    import random
    random.seed(42)  # Mindig fixáljuk a random seed-et a reprodukálhatóság miatt

    import string
    import timeit
    from itertools import islice, tee

    # A győztes n-gram készítő módszer az előző körből
    def ngram(iterator, n):
        return zip(*(islice(it, i, None) for i, it in enumerate(tee(iterator, n))))

    # Beállítások
    NUM_INPUTS = 10_000
    REPEAT = 7
    NUMBER = 100

    TEST_CASES = [
        {
            'name': '1 digit, 0 spaces',
            'leading_spaces': (0, 0),
            'freq_digits': (1, 1),
            'content_length': 50,
        },
        {
            'name': '1 digit, 1-5 spaces',
            'leading_spaces': (1, 5),
            'freq_digits': (1, 1),
            'content_length': 50,
        },
        {
            'name': '1 digit, 10-20 spaces',
            'leading_spaces': (10, 20),
            'freq_digits': (1, 1),
            'content_length': 50,
        },
        {
            'name': '6 digits, 0 spaces',
            'leading_spaces': (0, 0),
            'freq_digits': (6, 6),
            'content_length': 50,
        },
        {
            'name': '6 digits, 1-5 spaces',
            'leading_spaces': (1, 5),
            'freq_digits': (6, 6),
            'content_length': 50,
        },
        {
            'name': '6 digits, 10-20 spaces',
            'leading_spaces': (10, 20),
            'freq_digits': (6, 6),
            'content_length': 50,
        },
        {
            'name': '10 digits, 0 spaces',
            'leading_spaces': (0, 0),
            'freq_digits': (10, 10),
            'content_length': 50,
        },
        {
            'name': '10 digits, 1-5 spaces',
            'leading_spaces': (1, 5),
            'freq_digits': (10, 10),
            'content_length': 50,
        },
        {
            'name': '10 digits, 10-20 spaces',
            'leading_spaces': (10, 20),
            'freq_digits': (10, 10),
            'content_length': 50,
        },
        {
            'name': '6 digits, long content',
            'leading_spaces': (1, 5),
            'freq_digits': (6, 6),
            'content_length': 1000,
        },
        {
            'name': '6 digits, short content',
            'leading_spaces': (1, 5),
            'freq_digits': (6, 6),
            'content_length': 5,
        },
    ]

    def generate_data(n, leading_spaces_range, freq_digits_range, content_length):
        artificial_data = []

        for _ in range(n):
            leading_spaces = random.randint(*leading_spaces_range)

            num_digits = random.randint(*freq_digits_range)
            freq = random.randint(10 ** (num_digits - 1), 10 ** num_digits - 1)

            content = ''.join(random.choices(string.ascii_letters + string.digits + ' ', k=content_length))

            artificial_data.append(' ' * leading_spaces + str(freq) + ' ' + content)

        return artificial_data

    ###### A LÉNYEG: A módszerek ELEJE

    def method_find(input_data):
        for elem in input_data:
            freq_end = elem.find(' ', len(elem) - len(elem.lstrip(' ')))
            result_str = elem[:freq_end]

    def method_ngram(input_data):
        for elem in input_data:
            freq_end = next(n for n, char_bigram in enumerate(ngram(elem, 2), start=2)
                            if char_bigram[0].isnumeric() and char_bigram[1] == ' ')
            result_str = elem[:freq_end]

    mos_re = re.compile(' *[0-9]+ ')

    def method_re(input_data):
        for elem in input_data:
            result_str = mos_re.match(elem).group()

    ###### A LÉNYEG: A módszerek VÉGE

    def benchmark(test_name, input_data):
        find_times = timeit.repeat(lambda: method_find(input_data), repeat=REPEAT, number=NUMBER)
        ngram_times = timeit.repeat(lambda: method_ngram(input_data), repeat=REPEAT, number=NUMBER)
        re_times = timeit.repeat(lambda: method_re(input_data), repeat=REPEAT, number=NUMBER)

        find_best = min(find_times)
        ngram_best = min(ngram_times)
        re_best = min(re_times)

        return {'Test': test_name, 'find()': find_best, 'ngram()': ngram_best, 're()': re_best,
                'Speedup(ngram/find)': ngram_best / find_best, 'Speedup(re/find)': re_best / find_best}

    results = []

    for case in TEST_CASES:
        data = generate_data(n=NUM_INPUTS, leading_spaces_range=case['leading_spaces'],
                             freq_digits_range=case['freq_digits'], content_length=case['content_length'])

        result = benchmark(case['name'], data)
        results.append(result)

    print(f'\nInputs: {NUM_INPUTS:,} | repeat: {REPEAT} | number: {NUMBER}\n')

    header = (f'{"Test":<32}{"find() [s]":>14}{"ngram() [s]":>14}{"re() [s]":>14}{"Speedup(ngram/find)":>14}'
              f'{"Speedup(re/find)":>14}')
    print(header)
    print('-' * len(header))

    for result in results:
        print(f'{result["Test"]:<32}{result["find()"]:>14.6f}{result["ngram()"]:>14.6f}{result["re()"]:>14.6f}'
              f'{result["Speedup(ngram/find)"]:>11.2f}x{result["Speedup(re/find)"]:>11.2f}x')


def bla_bla_machine():
    import random
    from collections import defaultdict, Counter
    from itertools import islice, tee

    length = 100

    if True:
        n = 3                                   # TODO 5-gramnál és kellően nagy adatnál mókásak jönnek ki
        inp_data = str(list(range(1_000_000)))  # TODO Ide rendes szöveg fájlból ha érdekeset akarunk látni
        context = ('1', '2')                    # TODO itt n-1 darab elem kell
    else:
        n = 5
        # Feltéve, hogy van egy jól előkészített corpus.txt
        with open('corpus.txt', encoding='UTF-8') as fh:
            inp_data = fh.read()
        context = tuple(inpt_data.split(' ', maxspplit=5)[:5])

    # Model építése
    model = defaultdict(Counter)
    for ngram in zip(*(islice(it, i, None) for i, it in enumerate(tee(inp_data, n)))):
        model[ngram[:-1]][ngram[-1]] += 1

    # Generálás
    out = []
    for _ in range(length):
        if (counter := model.get(context)) is not None:
            word = random.choices(list(counter.keys()), weights=list(counter.values()), k=1)[0]
            out.append(word)
            context = (*context[1:], word)  # Kontextus ablak csúsztatása

    print(*out, sep='')


if __name__ == '__main__':
    exceptionok()
    path_kezeles()
    fajl_io()
    timeit_hasznalat()
    ngram_generator()
    meres2()
    bla_bla_machine()