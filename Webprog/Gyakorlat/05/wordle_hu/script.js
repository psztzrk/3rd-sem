/*
 * 1. feladat
 * Importáld a `delegate()` segédfüggvényt,
 * illetve word.js fájlból exportált deklarációkat!
 */
import {newWord} from "./word.js";
import {delegate} from "./delegate.js";

/*
 * 2. feladat
 * a) Tárold el konstansokban div#app-on belüli közvetlen gyermekeket!
 *    (elég csak azok ID-ji alapján)
 * b) Hozz létre egy `cursor` objektumot, amely tartalmazza a sor és oszlop indexét,
 *    ahova az új betű kerülne beírásra, kezdeti értéke legyen { row: 0, col: 0 }!
 */

const board = document.querySelector("#board");
const keyboard = document.querySelector("#keyboard");
const newGame = document.querySelector("#new-game");
const timerDisplay = document.querySelector("#timer");

let cursor = {row: 0, col: 0};
/*
 * 3. feladat
 * Egy billentyű megnyomásakor, ha még nem volt 6 tipp, akkor ha a gomb:
 * a) betű, akkor a megfelelő div-be írd be a betűt,  ha még van hely;
 * b) ←,    akkor töröld a megfelelő div-ből a betűt, ha már van betű;
 * c) ↲,    akkor ellenőrizd a beírd szót,            ha az már van 5 betű:
 *    - ha a szó helyes, azaz `guessWord()` nem null, akkor a megfelelő td-knek a megfelelő bg- class-t kell adnod és lépni új sorra;
 *    - ha a szó helytelen, azaz `guessWord()` null,  akkor az összes td-nek a bg-red class-t kell adnod 1 másodpercig.
 *
 * Ne felejtsd el frissíteni a `cursor` és `guessCount` segédváltozókat!
 * Használd az előbb importált `delegate()` segédfüggvényt!
 */
delegate(keyboard, "click", "td.keyboard.key", (event) => {
    if(cursor.row < 6){
        
    }
})


/*
 * 4. feladat
 * A "New Game" gomb megnyomásakor:
 * a) generálj egy új szót, illetve állítsd vissza a #board-ot és a `cursor` objektumot az eredeti állapotára;
 * b) indítsd újra a timer-t!
 */

