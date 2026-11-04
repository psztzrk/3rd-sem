#from typing import Literal
#from schemas.schema import Guest, Tab, Dish, Bill, DataStore, ReloadResult, MAX_DISCOUNT_PERCENT
from fastapi.responses import JSONResponse
from fastapi import HTTPException, APIRouter
#from fastapi import Query
#from pydantic import ValidationError
#from data.filehandler import add_guest, add_tab, add_dish_to_tab, update_dish_in_tab, remove_dish_from_tab, load_json_file, load_json_file_or_empty, save_json_file, merge_data, diff_counts
#from data.filereader import get_guest_by_id, get_tab_by_guest_id, get_dishes_by_guest_id, get_all_guests, get_bill, load_json

'''

Útmutató a fájl használatához:

- Minden route esetén adjuk meg a response_modell értékét (típus)
- Ügyeljünk a típusok megadására
- A függvények visszatérési értéke JSONResponse() legyen
- Minden függvény tartalmazzon hibakezelést, hiba esetén dobjon egy HTTPException-t
- Az adatokat a data.json fájlba kell menteni.
- A HTTP válaszok minden esetben tartalmazzák a
  megfelelő Státus Code-ot, pl. 201 - Created, 200 - OK, 400 - Bad Request,
  404 - Not Found, 409 - Conflict, 422 - Unprocessable Entity
- Az Enum mezőt tartalmazó modelleket model_dump(mode="json") hívással
  alakítsuk JSON-ná, így a kategória szövegként ("leves") kerül a fájlba.

'''

routers = APIRouter()

@routers.post('/addguest')
def addguest(guest):
    pass

@routers.post('/opentab')
def opentab(guestid: int, tableno: int) -> str:
    pass

@routers.post('/orderdish')
def orderdish(guestid: int, dish):
    pass

@routers.put('/updatedish')
def updatedish(guestid: int, dishid: int, dish):
    pass

@routers.delete('/canceldish')
def canceldish(guestid: int, dishid: int):
    pass

@routers.get('/guest')
def guest(guestid: int):
    pass

@routers.get('/guests')
def guests():
    pass

@routers.get('/tab')
def tab(guestid: int):
    pass

@routers.get('/getbill')
def getbill(guestid: int, discount: int = 0):
    pass

@routers.post('/save')
def save(source: str = "data.json", dest: str = "backup.json"):
    pass

@routers.post('/reload')
def reload(source: str = "backup.json", dest: str = "data.json", mode: str = "replace", keep_extra: bool = True):
    pass
