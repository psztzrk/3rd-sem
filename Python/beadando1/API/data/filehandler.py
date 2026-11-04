import copy
import json
import os
from typing import Dict, Any


'''
Útmutató a fájl függvényeinek a használatához

Új vendég hozzáadása:

new_guest = {
    "id": 4,  # Egyedi vendég azonosító
    "name": "Borász Barbara",
    "email": "barbara@pincesor.hu",
    "phone": "+36301112233"
}

Vendég hozzáadása a JSON fájlhoz:

add_guest(new_guest)

Számla (asztal) nyitása egy meglévő vendégnek:

new_tab = {
    "id": 104,  # Egyedi számla azonosító
    "guest_id": 4,  # Az a vendég, akihez a számla tartozik
    "table_no": 15,  # Az asztal száma
    "dishes": []  # Kezdetben üres számla
}

add_tab(new_tab)

Új étel rendelése egy vendég számlájára:

guest_id = 4
new_dish = {
    "dish_id": 205,
    "name": "Halászlé",
    "category": "leves",
    "price": 3290.0,
    "portions": 1
}

add_dish_to_tab(guest_id, new_dish)

Étel módosítása és törlése a számláról:

update_dish_in_tab(guest_id, 205, {...az étel új adatai...})
remove_dish_from_tab(guest_id, 205)

Mentés és visszatöltés tetszőleges (a data könyvtárban lévő) JSON fájlba/fájlból:

data = load_json_file("data.json")
save_json_file(data, "backup.json")

A get_file_path() csak egyszerű fájlnevet fogadjon el (könyvtárak nélkül),
.json kiterjesztéssel, és a data könyvtáron belüli elérési utat adja vissza.

A load_json_file_or_empty() ugyanaz, mint a load_json_file(), de nem létező fájl
esetén üres adatállományt ad vissza: {"Guests": [], "Tabs": []}

Visszatöltés összefésüléssel (merge):

merged = merge_data(current, backup, keep_extra=True)

 - current: a cél (data.json) jelenlegi tartalma, backup: a mentés tartalma
 - a mentésből csak azok a rekordok kerülnek be, amelyek a célban nincsenek meg:
     vendég: azonosító (id) alapján,
     számla: vendég (guest_id) alapján,
     étel: egy mindkét helyen meglévő számlán a dish_id alapján
 - a mindkét helyen meglévő rekordokból a cél (data.json) változata marad meg
 - keep_extra=True: a csak a célban lévő rekordok (vendég, számla, étel) megmaradnak
   keep_extra=False: a csak a célban lévő rekordok törlődnek
 - a bemenő adatokat a függvény nem módosíthatja (másolatot kell készíteni)

A változások összeszámolása (a visszatöltés előtti és utáni állapot összevetése):

changes = diff_counts(old, new)
# {"added":   {"guests": 1, "tabs": 1, "dishes": 3},
#  "removed": {"guests": 0, "tabs": 0, "dishes": 0},
#  "updated": {"guests": 0, "tabs": 0, "dishes": 1}}

 - added: az új állapotban meglévő, a régiben nem szereplő rekordok száma
 - removed: a régi állapotban meglévő, az újból hiányzó rekordok száma
 - updated: a mindkettőben meglévő, de eltérő tartalmú rekordok száma
   (a számlánál az ételek nélkül, csak az id és a table_no számít)
 - az ételeket a (guest_id, dish_id) pár azonosítja

Hogyan használd a fájlt?

Importáld a függvényeket a filehandler.py modulból:

from data.filehandler import (
    add_guest,
    add_tab,
    add_dish_to_tab,
)

 - Hiba esetén ValuErrort kell dobni, lehetőség szerint ezt a
   kliens oldalon is jelezni kell.

'''

DATA_DIR = os.path.dirname(__file__)
JSON_FILE_PATH = os.path.join(DATA_DIR, "data.json")

def load_json() -> Dict[str, Any]:
    pass

def save_json(data: Dict[str, Any]) -> None:
    pass

def get_file_path(filename: str) -> str:
    # Csak a data könyvtáron belüli .json fájlokat engedjük (pl. ../../main.py nem)
    pass

def load_json_file(filename: str) -> Dict[str, Any]:
    pass

def save_json_file(data: Dict[str, Any], filename: str) -> None:
    pass

EMPTY_DATA = {"Guests": [], "Tabs": []}

def load_json_file_or_empty(filename: str) -> Dict[str, Any]:
    pass

def merge_data(current: Dict[str, Any], backup: Dict[str, Any], keep_extra: bool = True) -> Dict[str, Any]:
    pass

def diff_counts(old: Dict[str, Any], new: Dict[str, Any]) -> Dict[str, Dict[str, int]]:
    pass

def add_guest(guest: Dict[str, Any]) -> None:
    pass

def add_tab(tab: Dict[str, Any]) -> None:
    pass

def add_dish_to_tab(guest_id: int, dish: Dict[str, Any]) -> Dict[str, Any]:
    pass

def update_dish_in_tab(guest_id: int, dish_id: int, dish: Dict[str, Any]) -> Dict[str, Any]:
    pass

def remove_dish_from_tab(guest_id: int, dish_id: int) -> Dict[str, Any]:
    pass
