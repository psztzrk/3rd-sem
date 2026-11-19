def pydantic_demo():
    # Pydantic v2 (!!!)
    # pip install pydantic[email]

    from pydantic import TypeAdapter, PositiveInt, ValidationError, EmailStr, BaseModel, field_validator, \
        model_validator, Field
    from typing import Optional
    from datetime import datetime

    inp = 1  # inp = input('Pozitív int: ')

    try:
        pi = TypeAdapter(PositiveInt).validate_python(inp)  # A PositiveInt(value) helyett
    except ValidationError:
        print('Nem pozitív int')
        exit(1)

    print('Valid pozitív int:', pi)

    # Ezért jobb:
    pi_list = TypeAdapter(list[PositiveInt]).validate_python(['1', '2', '3'])
    print(pi_list)

    # Email példa ------------------------------------------------------------------------------------------------------

    # RFC 5322, de nem valid:
    # 'al.ma+korte@host',
    # 'al.ma+korte@[192.168.1.1]'
    emailstr_list = TypeAdapter(list[EmailStr]).validate_python(['alma@korte.com', 'al.ma+korte@host.com'])
    print(emailstr_list)

    # Kompozit validálandó modell osztály alapon -----------------------------------------------------------------------
    class User(BaseModel):
        username: str
        email: EmailStr

    inp_email = 'alma@korte.com'  # inp_email = input('Email: ')
    inp_username = 'alma'  # inp_username = input('Username: ')

    try:
        user = User(username=inp_username, email=inp_email)
    except ValidationError as e:
        print('Nem validálható:\n', e)
        exit(1)

    print('User létrehozva:', user)

    # Haladó validációk ------------------------------------------------------------------------------------------------

    class User(BaseModel):
        # ... -> default=Required  (from pydantic import Required)
        # vs. default='default value' vagy default=None -> optionális, default értékkel
        # vs. username: str | None + model_dump(exclude_unset=True) -> Nem mutatja a modell a mezőt, ha nincs megadva
        username: str = Field(..., min_length=3)
        email: str
        password: str
        # Ez typingot használ semmi extra -> Sokféleképpen ki lehet fejezni a dolgokat
        signup_ts: Optional[datetime] = None
        is_active: bool = True
        opt: Optional[str] = None  # Ez az eltűnő opcionális

        # Field-level validation
        @field_validator('email')  # a @classmethod implicit hozzá lesz adva, ha explicit nem szerepel
        def email_must_have_at(cls, v):  # Ez még nem instance method
            if '@' not in v:
                raise ValueError('Email must contain @')
            return v.lower()  # az e-mail cím kisbetűssé alakítása (normalizáció)

        @model_validator(mode='before')
        def strip_strings(cls, values):
            # Ilyenkor (is) lehet normalizálni még a validálás előtt...
            for key, val in values.items():
                if isinstance(val, str):
                    values[key] = val.strip()
            return values

        @model_validator(mode='after')  # Pydantic 2.12 után így kell nem classmetoddal, a 3.0-val kompatibilitás miatt
        def check_password_strength(self):  # Pl. konzisztencia ellenőrzés
            # Ilyenkor már van egy fullos modellünk, amin lehet változtatni
            if len(self.password) < 6:
                raise ValueError('Password must be at least 6 characters')
            if self.password.lower() == self.username.lower():
                raise ValueError('Password must not be the same as username')
            return self  # Ez kötelező

    # Tesztinput
    data = {
        'username': '  Alice  ',
        'email': 'ALICE@EXAMPLE.COM  ',
        'password': 'alice123',
        'signup_ts': '2026-03-26T12:00:00'
    }

    try:
        user = User.model_validate(data)
    except ValidationError as e:
        print('Nem validálható:\n', e)
        exit(1)

    print(user.model_dump(exclude_unset=True))  # Normalizált, validált


def json_handling_demo():
    import json
    from pathlib import Path

    JSON_FILE = 'file.json'
    Path(JSON_FILE).write_text('[]')  # Létrehoz egy dummy fájlt a demó kedvéért

    # 1. Egysorban, egybe beolvasva a memóriába a tartalmat, lezárja a fájlt
    data = json.loads(Path(JSON_FILE).read_text(encoding='UTF-8'))  # A JSON belül UTF-8-al ugyanezt csinálná magától

    # 2. A JSON belül olvassa be a memóriába (és 'rb' mód esetén dekódol), de nem zárja le a fájlt
    #  Tehát json.load() -> json.loads(fh.read()) -> szükség esetén decode()-ot is futtat
    data = json.load(Path(JSON_FILE).open(encoding='UTF-8'))

    # 3. Ez is beolvassa egyben a memóriába és lezárja a fájlt. Gyak. mint az (1), de nem egy sor
    # with Path(JSON_FILE).open(encoding='UTF-8') as fh: is lehet ha sokat akarunk gépelni
    with open(JSON_FILE, encoding='UTF-8') as fh:
        data = json.load(fh)

    # 4. A fenti + exception handling
    try:
        # Python 3.15-től nem kell a encoding='UTF-8' mert megegyezik a default paraméterrel
        data = json.loads(Path(JSON_FILE).read_text(encoding='UTF-8'))

    except UnboundLocalError:
        print('JSON_FILE variable is not defined locally')

    except NameError:
        print('JSON_FILE variable is not defined locally or globally')

    except TypeError:
        print('JSON_FILE variable is not str or Path')

    except FileNotFoundError:
        print('File not found')

    except PermissionError:
        print('Permission denied')

    except IsADirectoryError:
        print('Expected a file but got a directory')

    except json.JSONDecodeError:  # Ez a ValueErrorból származik
        print('Invalid JSON format')

    except ValueError:
        print('General ValueError')

    except RecursionError:  # Ez a RuntimeErrorból származik
        print('Too deep recursion, limit exceeded')

    except RuntimeError:
        print('General Runtime error')

    except UnicodeDecodeError:
        print('Encoding issue while reading file')

    except ConnectionError:
        print('Connection error')

    except OSError as e:  # Kiválthatja a FileNotFoundError, PermissionError, IsADirectoryError és ConnectionError-t
        print(f'OS error: {e}')

    except MemoryError:
        print('Out of memory, file was too big')

    except SystemError:
        print('Bug in the Python interpreter itself')

    except Exception as e:
        print(f'Unexpected error happened: {e}')

    else:
        print('Loaded successfully')

    finally:
        print('Done')

    # 5. JSON írása + exception handling
    try:
        Path(JSON_FILE).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='UTF-8')
    except TypeError:
        print('Data contains non-serializable types')  # Új exception, ha nem lehet JSONosítani valamit (pl. set)
    except ValueError:
        print('Circular reference detected')  # Pl. a = []; a.append(a) JSON-osítása esetén...
        print('or Numerical representation error happened')  # float('inf'), float('nan') és allow_nan=False esetén
                                                             # Nem szabványos JSON, de a Javascript is támogatja
                                                             # Alapból allow_nan=True, szóval csak elméleti eshetőség
    except RecursionError:  # Lásd fent az olvasásnál
        print('Too deep recursion, limit exceeded')
    except PermissionError:
        print('Permission denied to write file')
    except IsADirectoryError:
        print('Expected a file path but got a directory')
    except FileExistsError:
        print('File is locked by the OS')
    except OSError as e:
        print(f'OS error: {e}')  # Pl. írás közben elfogyott a lemezen a hely
    else:
        print('JSON saved successfully')
    finally:
        print('Done')


def pickle_demo():
    import pickle

    # Bármilyen Python adattípus, nem úgy mint a JSON-nál
    user_data = {
        'name': 'Kovács János',
        'roles': ['admin', 'developer'],
        'preferences': {'theme': 'dark', 'notifications': True}
    }

    # Szerializálás: 'wb' módban, mert a pickle a JSON-nalszemben bináris adatot ír!
    with open('user_state.pkl', 'wb') as file:
        pickle.dump(user_data, file)

    # Beolvasás: Itt is 'wb' módban
    with open('user_state.pkl', 'rb') as file:
        loaded_data = pickle.load(file)

    assert user_data == loaded_data


def fastapi_demo():
    from fastapi import FastAPI, HTTPException, Request, Response, status
    from fastapi.responses import JSONResponse
    from contextlib import asynccontextmanager
    from pydantic import BaseModel, Field
    import uvicorn

    @asynccontextmanager
    async def app_lifespan(application: FastAPI):  # Itt async kell, hogy működjön, a többinél nem muszáj
        # Startup
        print('Starting application...')
        # Globális startup állapot az application.sate-ben menthető, mindenhol elérhető
        application.state.db = {'connected': True}
        print('Database connected!')

        yield  # Átadjuk a FastAPI-nak a futtatást

        # Shutdown
        print('Shutting down application...')
        print('Cleanup complete!')

    # Create FastAPI app with lifespan
    app = FastAPI(lifespan=app_lifespan)

    # Pydantic példa a POST requesthez
    class Item(BaseModel):
        name: str = Field(..., min_length=1)
        quantity: int = Field(..., ge=0)

    # Memóriabeli tárolóval szimuláljuk az adatbázist az egyszerűség kedvéért
    database = {}

    # GET endpoint
    @app.get('/items/{item_id}', response_model=Item)  # Ez végzi a tényleges ellenőrzést
    def get_item(item_id: int, response: Response) -> Item:  # Itt a visszatérés csak az IDE-nek szól

        # Minimális try blokk, nem itt van a return vagy a tényleges adatfeldolgozás!
        try:
            item_value = database[item_id]
        except KeyError:
            raise HTTPException(status_code=404, detail='Item not found')  # Hiba

        # Ha ezt csináljuk, a FastAPI úgy veszi, hogy manuálisan ellenőriztünk. -> Nincs használva a Pydantic
        # Saját headerek + status code beállítása
        """
        return JSONResponse(content={'item_id': item_id, 'data': item_value},
                            status_code=200,  # Ez a default, illik elhagyni, mert különben zavaró
                            headers={'X-Custom-Header': 'FastAPI-Example'})
        """

        # Saját header beállítása az injektált response objektumon keresztül
        response.headers['X-Custom-Header'] = 'FastAPI-Example'

        # Közvetlenül a modellt vagy a dict-et adjuk vissza, a FastAPI ellenőrzi a response_model alapján
        return Item(name=str(item_id), quantity=item_value['quantity'])

    # POST endpoint
    # Csak akkor kell 201 ha a Location headert is visszaadjuk, amúgy 200
    @app.post('/items/', status_code=status.HTTP_201_CREATED, response_model=Item)
    def create_item(item: Item, response: Response) -> Item:
        if item.name in database:
            raise HTTPException(status_code=400, detail='Item already exists')
        # Mentés az 'adatbázisba'
        database[item.name] = {'quantity': item.quantity}

        """
        return JSONResponse(content={'message': 'Item created', 'item': database[item.name]},
                            status_code=201,
                            headers={'Location': f'/items/{item.name}'})
        """

        # A Location header beállítása (kijavítva a felesleges kettőspont a stringen belül)
        response.headers['Location'] = f'/items/{item.name}'

        # Visszaadjuk a beérkezett és ellenőrzött Pydantic objektumot
        return item

    # Global exception handler (opcionális) saját hibakezelést tesz lehetővé
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(status_code=exc.status_code,
                            content={'error': exc.detail, 'custom': True},
                            # Itt a custom true eltűnik a hibánál ha ezt a kódot töröljük
                            headers={'X-Error-Handled': 'true'})

    # Így futtatható az applikáció
    """
    if __name__ == '__main__':
        import uvicorn

        uvicorn.run('gyak7:app', host='127.0.0.1', port=8000, reload=True)
    """

    return app


if __name__ == '__main__':
    pydantic_demo()
    # json_handling_demo()
    # pickle_demo()


app = fastapi_demo()

# Ne feledjük megnézni a SWAGGER-t: http://127.0.0.1:8000/docs
if __name__ == '__main__':
    import uvicorn

    uvicorn.run('gyak7:app', host='127.0.0.1', port=8000, reload=True)

