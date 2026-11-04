import re
from enum import Enum
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from typing import List, Literal

'''

Útmutató a fájl használatához:

Az osztályokat a schema alapján ki kell dolgozni.

A schema.py az adatok küldésére és fogadására készített osztályokat tartalmazza.
Az osztályokban az adatok legyenek validálva.
 - az int adatok nem lehetnek negatívak.
 - az email mező csak e-mail formátumot fogadhat el.
 - a telefonszám formátuma: +36 és utána 9 számjegy (pl. +36301234567);
   a szóközöket és kötőjeleket a validálás előtt el kell távolítani.
 - az ár pozitív szám, az adag 1 és 20 közötti egész szám.
 - az asztalszám 1 és 30 közötti egész szám.
 - az étel kategóriája csak a következő értékek egyike lehet:
   "leves", "előétel", "főétel", "desszert", "ital"
   -> készíts hozzá egy Category nevű Enum osztályt (lásd a feladatleírást),
      és a Dish.category mező típusa ez legyen.
 - egy számlán egy étel (dish_id) csak egyszer szerepelhet (modell szintű
   validáció, lásd: @model_validator a feladatleírásban).
 - a teljes adatállomány (DataStore) legyen ellentmondásmentes (modell szintű validáció):
   egyedi vendég- és számla-azonosítók, egy vendégnek legfeljebb egy számlája van, egy
   asztalhoz legfeljebb egy számla tartozik, és minden számla létező vendéghez tartozik.
 - Hiba esetén ValueErrort kell dobni, lehetőség szerint ezt a
   kliens oldalon is jelezni kell.

'''

RestaurantName = 'Pythonia Bisztró'

SERVICE_CHARGE_PERCENT = 12
MAX_TABLE_NO = 30
MAX_PORTIONS = 20
MAX_DISCOUNT_PERCENT = 50


class Dish(BaseModel):
    dish_id: int
    name: str
    category: str
    price: float
    portions: int


class Tab(BaseModel):
    id: int
    guest_id: int
    table_no: int
    dishes: List[Dish]


class Guest(BaseModel):
    id: int
    name: str
    email: str
    phone: str


class Bill(BaseModel):
    guest_id: int
    table_no: int
    subtotal: float
    service_charge: float
    discount_percent: int
    discount_amount: float
    total: float


class DataStore(BaseModel):
    '''A data.json teljes tartalma - a mentés és visszatöltés ellenőrzéséhez.'''
    Guests: List[Guest]
    Tabs: List[Tab]


class ChangeCount(BaseModel):
    '''A visszatöltés során megváltozott rekordok száma fajtánként.'''
    guests: int
    tabs: int
    dishes: int


class ReloadResult(BaseModel):
    '''A /reload végpont válasza.'''
    message: str
    source: str
    dest: str
    mode: str          # -> Literal["replace", "merge"]
    keep_extra: bool
    added: ChangeCount
    removed: ChangeCount
    updated: ChangeCount
