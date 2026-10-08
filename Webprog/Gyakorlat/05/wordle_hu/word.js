/*
 * 1. feladat
 * Importáld a `words` változót a data.js fájlból!
 */
import { words } from "./data.js";


/*
 * 2. feladat
 * Készíts `word` nevű változót a kitalálandó szó eltárolására,
 * melynek kezdeti értéke legyen null!
 */
let word = null;


/*
 * 3. feladat
 * Implementálj egy (paraméter nélküli) `newWord()` eljárást,
 * amely választ egy új szót a szótárból és azt értékül adja a `word` változónak!
 */

function newWord(){
    word = words[Math.floor(Math.random() * words.length)];
}


/*
 * 4. feladat
 * Implementálj egy `guessWord(guess)` függvényt,
 * ahol a paraméter az 5 karakterből álló tipp, és ha
 * - létező szó a `guess`, akkor visszaad egy 5 string-et tartalmazó tömböt;
 * - ellenben visszaad egy null értéket.
 * Az 5 string-et tartalmazó tömb elemei:
 * - "green" - az adott karakter helyes és jó helyen van,
 * - "yellow" - az adott karakter helyes, de nem a megfelelő helyen,
 * - "gray" - az adott karakter helytelen.
 * Ha `word` null, akkor először hívd meg a newWord()-öt!
 *
 * Pl.: word = "abcde" és guess = "ABEFG",
 * akkor a visszaadott tömb: ["green", "green", "yellow", "gray", "gray"].
 * Használd a guess.toLowerCase() függvényt a tipp kisbetűzéséhez!
 */
function guessWord(guess){
    if(word === null) newWord();
    guess = guess.toLowerCase();

    if (words.includes(guess)) return null;

    return guess.split("").map((char, index) => {
        if (char === word[index]) {
            return "green";
        }
        else if( word.includes(char))
            return "yellow";
        else
            return "grey";
    })

}


/*
 * 5. feladat
 * Exportáld a `newWord` és a `guessWord` deklarációkat!
 */