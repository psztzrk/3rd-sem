/*
 * 1. feladat
 * Ellenőrizd, hogy beküldéskor:
 * - #name és #hobby kitöltésre került-e,
 * (input.value == "")
 * - #age számmal került-e kitöltésre,
 * - #gender rádiógombjaiból valamelyik került-e kiválasztásra.
 * Hiba esetén akadályozd meg az űrlap beküldését,
 * és jelenítsd meg az(oka)t az #errors listában.
 *
 * Gondolatmenet:
 * - kérdezd le az összes elemet,
 *   amelyekre szükség van az eseménykezeléshez és hibaellenőrzéshez
 * - a formon való "submit" eseményekor:
 *   - deklarálj egy tömböt a hibák gyűjtéséhez;
 *   - ellenőrizd mezőnként egy-egy elágazásban, hogy van-e hiba,
 *     ha igen azt add hozzá a tömbhöz;
 *   - ha van hiba, akkor akadályozd meg a beküldést
 *     és jelenítsd meg a hibákat (illetve töröld az előzőeket).
 */ 

const nameInput = document.querySelector("#name");
const ageInput = document.querySelector("#age");
