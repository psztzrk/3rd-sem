import json
import os
from typing import Dict, Any, List

'''
Útmutató a fájl használatához:

Vendég adatainak lekérdezése:

guest_id = 1
guest = get_guest_by_id(guest_id)
print(f"Vendég adatai: {guest}")

Vendég számlájának (teljes rekord) lekérdezése:

tab = get_tab_by_guest_id(guest_id)
print(f"Vendég számlája: {tab}")

Vendég által rendelt ételek lekérdezése:

dishes = get_dishes_by_guest_id(guest_id)
print(f"Rendelt ételek: {dishes}")

Összes vendég lekérdezése:

guests = get_all_guests()
print(f"Összes vendég: {guests}")

Vendég végösszegének (számlájának) kiszámítása 10% kedvezménnyel:

bill = get_bill(guest_id, 10)
print(f"Számla: {bill}")

A számla kiszámítása (minden összeg két tizedesjegyre kerekítve):
 - subtotal: sum(ár * adag) a számlán lévő ételekre
 - service_charge: a subtotal 12%-a
 - discount_amount: (subtotal + service_charge) * kedvezmény% / 100
 - total: subtotal + service_charge - discount_amount

Hogyan futtasd?

Importáld a függvényeket a filereader.py modulból:

from data.filereader import (
    get_guest_by_id,
    get_tab_by_guest_id,
    get_dishes_by_guest_id,
    get_all_guests,
    get_bill
)

 - Hiba esetén ValuErrort kell dobni, lehetőség szerint ezt a
   kliens oldalon is jelezni kell.

'''

# A JSON fájl elérési útja
JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), "data.json")

SERVICE_CHARGE_PERCENT = 12

def load_json() -> Dict[str, Any]:
    pass

def get_guest_by_id(guest_id: int) -> Dict[str, Any]:
    pass

def get_tab_by_guest_id(guest_id: int) -> Dict[str, Any]:
    pass

def get_dishes_by_guest_id(guest_id: int) -> List[Dict[str, Any]]:
    pass

def get_all_guests() -> List[Dict[str, Any]]:
    pass

def get_bill(guest_id: int, discount_percent: int = 0) -> Dict[str, Any]:
    pass
