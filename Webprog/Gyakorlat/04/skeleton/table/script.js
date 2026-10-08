// delegate segédfüggény
function delegate(parent, type, selector, handler) {
  parent.addEventListener(type, function (event) {
    const targetElement = event.target.closest(selector);
    if (this.contains(targetElement)) handler.call(targetElement, event);
  });
}

/*
 * 1. feladat
 * A "New Game" gombra kattintáskor generálj a megadott sor és oszlopszámnak
 * megfelelően, a meglévő táblázat helyére.
 * Az így generált táblázat celláinak egyikének legyen a tartalma "X".
 *
 * Gondolatmenet:
 * - kérdezz le minden elemet, amelyre a feladat megoldásához szükség lesz
 * - a #new-game gombra való "click" eseménykor:
 *   - parse-old megadott sor és oszlopszámot számmá (parseInt());
 *   - generálj egy kétdimenziós indexet, amelybe majd belekerül az "X";
 *   - töröld a táblázat eddigi tartalmát;
 *   - "kétdimenziós" ciklus segítségével generálj egy sorokat és oszlopokat,
 *     amelyekhez add hozzá a megfelelő stílusosztályokat
 *     (sornak board-row és cellának board-cell és bg-gray),
 *     majd add hozzá az elemet a megfelelő szülőhöz (cellákat sorhoz, sorokat táblázathoz).
 */

const row = document.querySelector("#row");




function randomInteger(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

/*
 * 2. feladat
 * Az egyes cellákra kattintáskor, ha az tartalmazza a bg-gray stílusosztályt, akkor:
 * - ha az tartalmazza az "X"-et, az legyen sárga (bg-yellow stílusosztály);
 * - ellenben legyen zöld (bg-green stílusosztály).
 * Használd a delegate() segédfüggvényt!
 */
