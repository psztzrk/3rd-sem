# pip install 'sqlalchemy>=2.0,<3.0'

from sqlalchemy import ForeignKey, String, Integer, Table, Column, MetaData, create_engine, insert, select, update, \
    delete, func, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session, selectinload

# SQLite memóriabeli adatbázis
# Más adatbázisokhoz például:
# SQLite fájl: sqlite+pysqlite:///db.sqlite
# PostgreSQL:  postgresql+psycopg://felhasznalo:jelszo@localhost/adatbazis
# MySQL:       mysql+pymysql://felhasznalo:jelszo@localhost/adatbazis

# echo=True esetén a SQLAlchemy kiírja a generált SQL utasításokat
engine = create_engine('sqlite+pysqlite:///:memory:', echo=False)

print('Engine létrehozva:', engine)

# CORE -----------------------------------------------------------------------------------------------------------------
"""
A Core megközelítésben közvetlenül definiálhatunk adatbázistáblákat

    - Táblákkal és SQL-kifejezésekkel dolgozunk
    - A lekérdezések szerkezete közel áll a hagyományos SQL-hez
    - Jó választás lehet összetett SQL-műveletekhez és adatorientált feladatokhoz
    - Példa: select(employees).where(employees.c.salary > 600000)

Itt nem szükséges Python ORM-osztályt létrehozni
"""

# Táblák és metaadatok
core_metadata = MetaData()

# Így készülnek az auto_increment-ek házilag ( default constraint, lásd lejebb)
i = 0


def mydefault():
    global i
    i += 1
    return i


departments = Table('departments', core_metadata,
                    Column('id', Integer, primary_key=True),
                    Column('name', String(100), nullable=False, unique=True))  # , default=mydefault

employees = Table('employees', core_metadata,
                  Column('id', Integer, primary_key=True),
                  Column('name', String(100), nullable=False),
                  Column('salary', Integer, nullable=False),
                  Column('department_id', ForeignKey('departments.id')))

# A Core táblák tényleges létrehozása
core_metadata.create_all(engine)

# INSERT, SELECT, UPDATE, DELETE

# INSERT - új rekordok beszúrása
with engine.begin() as connection:
    # INSERT INTO departments (name) VALUES (?)
    connection.execute(insert(departments), [{'name': 'Informatika'},
                                             {'name': 'Matematika'},
                                             {'name': 'Fizika'}])

    # INSERT INTO employees (name, salary, department_id) VALUES (?, ?, ?)
    connection.execute(insert(employees), [{'name': 'Anna', 'salary': 650000, 'department_id': 1},
                                           {'name': 'Béla', 'salary': 590000, 'department_id': 1},
                                           {'name': 'Csilla', 'salary': 720000, 'department_id': 2},
                                           {'name': 'Dávid', 'salary': 610000, 'department_id': 3}])

# SELECT - minden dolgozó lekérdezése
# SELECT employees.name, employees.salary FROM employees
stmt = select(employees)
with engine.connect() as connection:
    result = connection.execute(stmt)
    print('Dolgozók:')
    for row in result:
        print(dict(row._mapping))

# WHERE és ORDER BY - szűrés és rendezés
# SELECT employees.name, employees.salary FROM employees WHERE employees.salary >= ? ORDER BY employees.salary DESC
stmt = select(employees.c.name, employees.c.salary). \
    where(employees.c.salary >= 600_000). \
    order_by(employees.c.salary.desc())

with engine.connect() as connection:
    print('Legalább 600 000 fizetésű dolgozók:')
    for row in connection.execute(stmt):
        print(row.name, '-', row.salary)

# JOIN - több tábla összekapcsolása
# SELECT employees.name AS employee, departments.name AS department
# FROM employees JOIN departments ON employees.department_id = departments.id
stmt = select(employees.c.name.label('employee'), departments.c.name.label('department')). \
    select_from(employees.join(departments, employees.c.department_id == departments.c.id))

with engine.connect() as connection:
    print('Dolgozók és részlegeik (JOIN):')
    for row in connection.execute(stmt):
        print(f'{row.employee} - {row.department}')

# UPDATE - rekord módosítása
with engine.begin() as connection:
    # UPDATE employees SET salary=? WHERE employees.name = ?
    result = connection.execute(update(employees). \
                                where(employees.c.name == 'Béla'). \
                                values(salary=630000))
    print('Módosított rekordok száma:', result.rowcount)

# DELETE - rekord törlése
# A példában egy külön tesztrekordot szúrunk be, majd törlünk
with engine.begin() as connection:
    # INSERT INTO employees (name, salary, department_id) VALUES (?, ?, ?)
    connection.execute(insert(employees). \
                       values(name='Teszt Elek', salary=100000, department_id=1))
    # DELETE FROM employees WHERE employees.name = ?
    result = connection.execute(delete(employees). \
                                where(employees.c.name == 'Teszt Elek'))
    print('Törölt tesztrekordok száma:', result.rowcount)

# Aggregáció, GROUP BY és paraméterezett SQL
# SELECT departments.name AS department, count(employees.id) AS employee_count, avg(employees.salary) AS average_salary
# FROM departments LEFT OUTER JOIN employees ON departments.id = employees.department_id
# GROUP BY departments.id, departments.name ORDER BY departments.name
stmt = select(departments.c.name.label('department'),
              func.count(employees.c.id).label('employee_count'),
              func.avg(employees.c.salary).label('average_salary')). \
    select_from(departments.outerjoin(employees, departments.c.id == employees.c.department_id)). \
    group_by(departments.c.id, departments.c.name). \
    order_by(departments.c.name)

with engine.connect() as connection:
    print('Részlegenkénti statisztika:')
    for row in connection.execute(stmt):
        print(f'{row.department}: {row.employee_count} dolgozó, átlagfizetés: {row.average_salary:.0f}')

# Paraméterezett, szöveges SQL

# A text() használatával hagyományos SQL-t is végrehajthatunk
# A paramétereket mindig kötött paraméterként adjuk át, ne string összefűzéssel építsük be az SQL-be (lásd következő)
with engine.connect() as connection:
    result = connection.execute(text('SELECT name, salary FROM employees WHERE salary > :minimum'),
                                {'minimum': 700000})
    print('Nyers SQL text() használatával:')
    for row in result:
        print(row.name, row.salary)

with engine.connect() as connection:
    # SQL injection lásd még Bobby tables: https://xkcd.com/327/
    # SELECT name, salary FROM employees WHERE salary > 700000; DROP TABLE employees;
    # minimum = '700000; DROP TABLE employees; --'
    # Szerencsére le van korlátozva és csak egy statement-et lehet így megadni, különben hibát ad

    # SELECT name, salary FROM employees WHERE salary > 700000 OR 1=1
    minimum = '700000 OR 1=1'

    # Ez így veszélyes! Még ha text()-be is van wrappolva!
    sql = text(f'SELECT name, salary FROM employees WHERE salary > {minimum}')

    result = connection.execute(sql)

    print('Eredmény:')
    for row in result:
        print(row.name, row.salary)

# ORM - deklaratív modellek --------------------------------------------------------------------------------------------
"""
Az ORM esetén Python osztályokat rendelünk adatbázistáblákhoz (az ORM a Core funkcionalitására épül)
    - Python osztályokat rendelünk az adatbázistáblákhoz
    - A rekordokat Python objektumokként kezeljük
    - A Session követi az objektumok állapotát és kezeli a tranzakciókat
    - A kapcsolatok objektumokon keresztül is bejárhatók
    - Példa: select(User).where(User.name == 'Kovács Anna')

Mindkét megközelítés ugyanannak a SQLAlchemy könyvtárnak a része
"""


class Base(DeclarativeBase):
    """
    A Base közös ősosztály tárolja a modellek metaadatait
    Hasonló mint fent a core_metadata = MetaData()

    Lásd később:
    Base.metadata.create_all(engine)
    """

    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)

    # Egy felhasználónak több bejegyzése lehet
    posts: Mapped[list['Post']] = relationship(back_populates='author', cascade='all, delete-orphan')

    def __repr__(self):
        return f'User(id={self.id}, name={self.name!r}, email={self.email!r})'


class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(String(1000), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    # A bejegyzés szerzője
    author: Mapped['User'] = relationship(back_populates='posts')

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title!r}, user_id={self.user_id})'


# Az ORM-modellekhez tartozó táblák tényleges létrehozása
Base.metadata.create_all(engine)

# CREATE és READ (Session)

# A Session az ORM-műveletek központi objektuma
# Kezeli az objektumok állapotát, a tranzakciókat és az adatbázis-műveleteket
with Session(engine) as session:
    # Python objektumok létrehozása
    user1 = User(name='Kovács Anna', email='anna@example.com')
    user2 = User(name='Nagy Béla', email='bela@example.com')

    # Kapcsolat létrehozása objektumon keresztül
    user1.posts = [Post(title='Bevezetés az adatbázisokba', content='Az adatbázisok alapfogalmai és relációs modellje'),
                   Post(title='SQL alapok', content='SELECT, INSERT, UPDATE és DELETE műveletek')]

    user2.posts = [Post(title='Python programozás', content='Osztályok, objektumok és adatkezelés')]

    session.add_all([user1, user2])

    # A tranzakció véglegesítése
    session.commit()

    print('Létrehozott felhasználó:', user1)
    print('Generált azonosító:', user1.id)

    # SELECT - ORM lekérdezés a 2.x stílusban
    # SELECT users.id, users.name, users.email FROM users ORDER BY users.name
    stmt = select(User).order_by(User.name)
    # Itt csak egy "oszlopot" (teljes User rekord) kérdezünk le (scalars)
    # Létezik a .scalar() -is pl a COUNT() meg AVG() esetekre, ahol egy elem van csak
    users = session.scalars(stmt).all()

    print('Felhasználók:')
    for user in users:
        print(user)

    # WHERE - feltételes lekérdezés
    # SELECT users.id, users.name, users.email FROM users WHERE users.name = ?
    stmt = select(User).where(User.name == 'Kovács Anna')
    anna = session.scalars(stmt).first()
    print('Név alapján keresett felhasználó:', anna)

# Kapcsolatok és JOIN

with Session(engine) as session:
    # Kapcsolt objektumok elérése
    # SELECT users.id, users.name, users.email FROM users WHERE users.email = ?
    stmt = select(User).where(User.email == 'anna@example.com')
    # Az .one() csak egy elemet ad vissza vagy exceptiont ha több elem is lenne
    # A .one_or_none() megengedi a 0 elem visszatérítését
    # A .first() lekérdezi az összes elemet, de csak az elsőt téríti vissza, a többit eldobja
    anna = session.scalars(stmt).one()

    print(f'{anna.name} bejegyzései:')
    # Implicit átugrottunk a posts tábla lekérdezésére
    # SELECT posts.id, posts.title, posts.content, posts.user_id FROM posts WHERE ? = posts.user_id
    for post in anna.posts:
        print(' -', post.title)

    # JOIN - felhasználók és bejegyzések összekapcsolása
    # SELECT users.name, posts.title FROM users JOIN posts ON users.id = posts.user_id ORDER BY users.name, posts.title
    stmt = select(User.name, Post.title). \
        join(Post, User.id == Post.user_id). \
        order_by(User.name, Post.title)

    print('JOIN eredménye:')
    # Ugyebár itt több oszlopot (User.name, Post.title) kérdeztünk le (execute)
    for row in session.execute(stmt):
        print(f'{row.name}: {row.title}')

    # selectinload: kapcsolt objektumok előzetes betöltése
    # Nagyobb adatmennyiségnél segíthet elkerülni az N+1 lekérdezési problémát
    # SELECT users.id, users.name, users.email FROM users
    # SELECT posts.user_id, posts.id, posts.title, posts.content FROM posts WHERE posts.user_id IN (?, ?)
    stmt = select(User).options(selectinload(User.posts))
    users = session.scalars(stmt).all()

    print('Felhasználók előre betöltött bejegyzésekkel:')
    for user in users:
        print(user.name, '- bejegyzések száma:', len(user.posts))

# UPDATE, DELETE, aggregáció és tranzakció

with Session(engine) as session:
    # UPDATE - objektum módosítása
    # SELECT users.id, users.name, users.email FROM users WHERE users.email = ?
    stmt = select(User).where(User.email == 'bela@example.com')
    bela = session.scalars(stmt).one()

    # Béla itt UPDATE-elődik
    bela.name = 'Nagy Béla (módosítva)'
    session.commit()
    print('Módosított felhasználó:', bela)

    # Aggregáció ORM-lekérdezéssel
    # SELECT count(users.id) AS count_1 FROM users
    stmt = select(func.count(User.id))
    user_count = session.scalar(stmt)
    print('Felhasználók száma:', user_count)

    # SELECT count(posts.id) AS count_1 FROM posts
    stmt = select(func.count(Post.id))
    post_count = session.scalar(stmt)
    print('Bejegyzések száma:', post_count)

    # DELETE - objektum törlése
    # A cascade='all, delete-orphan' miatt a kapcsolt bejegyzések is törlődnek
    # SELECT users.id, users.name, users.email FROM users WHERE users.email = ?
    stmt = select(User).where(User.email == 'bela@example.com')
    user_to_delete = session.scalars(stmt).one()

    # DELETE FROM posts WHERE posts.id = ?
    session.delete(user_to_delete)
    session.commit()
    print('A második felhasználó és bejegyzései törölve')

    """
    vs.
    stmt = delete(User).where(User.email == 'bela@example.com')
    result = session.execute(stmt)
    session.commit()
    
    Itt nincs objektum, nem törli a kapcsolt bejegyzéseket!   
    """

# TRANZAKCIÓ - commit és rollback

with Session(engine) as session:
    try:
        # A session.begin() tranzakciós kontextust nyit
        # Siker esetén commit, kivétel esetén rollback történik
        with session.begin():
            temporary_user = User(name='Ideiglenes felhasználó', email='temporary@example.com')
            session.add(temporary_user)

            # Szándékosan kiváltott hiba a rollback bemutatásához
            raise RuntimeError('Szimulált hiba - a tranzakció visszagörgetése')

    except RuntimeError as error:
        print('Hiba:', error)
        print('A tranzakció rollback művelettel visszaállt')

    # Ellenőrizzük, hogy a rekord nem került be az adatbázisba
    # SELECT users.id, users.name, users.email FROM users WHERE users.email = ?
    stmt = select(User).where(User.email == 'temporary@example.com')
    temporary = session.scalars(stmt).first()

    print('Az ideiglenes felhasználó létezik?', temporary is not None)
