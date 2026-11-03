# Webprog JavaScript ZH

**1.** adatlekérdezés, 
**2.** űrlap, lista és interaktív táblázat, 
**3.** rács, kattintás, delegálás. 

## Ellenőrzőlista és gyakori hibák

Egyetlen hiba az egész scriptet megállítja, és az utána jövő részfeladatok pontjai is elvesznek. Mindig figyeld a konzolt (F12 → Console), és ami nem működik, azt beadás előtt kommenteld ki.

| Hibaüzenet | Ok | Javítás |
| `Cannot set properties of null` | rossz szelektor, vagy a script túl korán fut | nézd meg az id-t (`#` elöl), a script a body végén legyen |
| `Assignment to constant variable` | `elem = ...` az `elem.innerText = ...` helyett | `.innerText` / `.value` kell |
| `X is not defined` | elírt név, vagy a változót a függvényén / `forEach`-én kívül használod | név, hatókör ellenőrzése |
| `X is not a function` | zárójel egy nem-függvény után, pl. `author.books(...)` | lemaradt a metódus: `author.books.some(...)` |
| `Cannot read properties of undefined` | tömbtől kéred az elemei mezőjét, pl. `books.genres` | `some` / `map` a tömbön |
| `NaN` a kiírásban | objektumot adsz össze (`acc + x`), vagy üres input | `acc + x.pages`, `Number(...)` |
| `undefined` a kiírásban | `filter(...).title` vagy elírt mezőnév | `find(...).title` vagy `.map(x => x.title)` |

- `.value`: input, select, textarea. `.innerText`: minden más elem.
- Az `input.value` mindig string: `Number(...)`. Csak a `+` fűz össze, a `- * /` számol.
- `addEventListener`, `setInterval`: a függvényt zárójel nélkül add át.
- Többsoros nyílfüggvény: `{ }` kell, és ha értéket ad, `return` is.
- `===`, nem `==`. ID-k, osztálynevek, üzenetek betűre pontosan: a teszt szó szerint nézi.
- Igaz/hamis eredményt egy próbalépéssel is ellenőrizz: a véletlenül jó `false` gyakori.

## 1. feladat – adatlekérdezés

Minden részfeladat egy kérdés az adatokról, a válasz egy `taskX` elembe kerül. Fogalmazd meg magyarul, keresd meg a kulcsszót, és belülről kifelé építsd fel, minden lépést `console.log`-gal ellenőrizve.

| Ha a feladat ezt kéri | Használd | Látott példa |
| egy olyan elem (neve, címe) | `find(...).mező` | egy 2000 előtti videó címe |
| azok listája | `filter` + `map` + `join(", ")` | 100 millió fölötti videók |
| hány darab | `filter(...).length` | hány címben van „Love” |
| van-e olyan | `some` | van-e számjegyes dalcím |
| mindegyikre igaz-e | `every` | minden szerzőnek van-e regénye |
| egy elemen belül legalább N | belső `filter(...).length >= N` | szerző ≥ 2 régi könyvvel |
| összesen | `reduce` | összes oldalszám |
| átlag, N tizedes | szurt összeg / szurt hossz, `toFixed(N)` | 2024-es videók átlaga |
| a legtöbb / legnagyobb | maximumkeresés, szigorú `>` | legtöbb oldalt író szerző |
| tömb a tömbben, együtt | `flatMap` | minden szerző minden könyve |
| több feltétel egyszerre | `&&` | 1900 előtti ÉS regény |
| szöveg egy része | `split(" - ")[1]` | a dalcím a kötőjel után |
| kis- és nagybetűtől független | `toLowerCase()` mindkét oldalon |  |
| különböző értékek | `new Set(...)` | hány különböző év |

```js
// EGY ELEM egy mezője: „egy 2000 előtti videó címe” (find egy objektumot ad, .title nélkül [object Object])
taskA.innerText = data.find(v => v.year < 2000).title;

// BELÜLRŐL KIFELÉ: előbb egy elemre, aztán a külső metódusba (authors[0] → a)
console.log(authors[0].books.filter(b => b.year < 1900).length >= 2);
taskA.innerText = authors.some(a => a.books.filter(b => b.year < 1900).length >= 2);

// KÉT SZINT: „minden szerzőnek van regénye”
taskB.innerText = authors.every(a => a.books.some(b => b.genres.includes("regény")));

// LISTA: „azok nevei, akiknek van 500+ oldalas regénye”
taskC.innerText = authors
    .filter(a => a.books.some(b => b.pages > 500 && b.genres.includes("regény")))
    .map(a => a.name)
    .join(", ");

// ÖSSZEG beágyazott adatból
const osszes = authors.flatMap(a => a.books);
taskD.innerText = osszes.reduce((acc, b) => acc + b.pages, 0);

// ÁTLAG: ugyanannak a szűrt tömbnek az összege / hossza
const szurt = osszes.filter(b => b.year < 1900 && b.genres.includes("regény"));
taskF.innerText = (szurt.reduce((acc, b) => acc + b.pages, 0) / szurt.length).toFixed(2);

// MAXIMUM: segédfüggvény + szigorú > (holtversenyben az első marad)
function oldalszam(a) { return a.books.reduce((acc, b) => acc + b.pages, 0); }
let legjobb = authors[0];
for (const a of authors)
    if (oldalszam(a) > oldalszam(legjobb)) legjobb = a;
taskE.innerText = legjobb.name;

// SZÖVEGVIZSGÁLAT: „van-e számjegyes dalcím” (csak a kötőjel utáni rész)
const szamjegyek = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"];
taskE.innerText = data.some(v => {
    const dalcim = v.title.split(" - ")[1];
    return szamjegyek.some(d => dalcim.includes(d));
});

// MAXIMUM, ha az érték kész mező: „a legnézettebb videó címe”
let top = data[0];
for (const v of data)
    if (v.views > top.views) top = v;
taskX.innerText = top.title;

// csak a legnagyobb ÉRTÉK kell, nem az elem
Math.max(...data.map(v => v.views))     // 295

// KÜLÖNBÖZŐ ÉRTÉKEK
[...new Set(data.map(v => v.year))]     // az egyedi évek tömbje
new Set(data.map(v => v.year)).size     // hány különböző év (.size, nem .length!)
new Set(authors.flatMap(a => a.books).flatMap(b => b.genres)).size   // hány féle műfaj
```

## 2. feladat – űrlap, lista, interaktív táblázat

Gombok, mezők, csúszkák, legördülő lista: minden vezérlőre közvetlen `addEventListener`. Ha egy lista vagy táblázat az adatokból épül, állapot + `render()`: az esemény csak az adatot módosítja, utána minden újrarajzolódik.

| Ha a feladat ezt kéri | Használd |
| gombra új elem a listába | `push` + `render()` |
| szóközök levágása, üres tiltása | `value.trim()`, `if (uj === "") return;` |
| ne legyen ismétlődés (kis-nagybetű mindegy) | `some(x => x.toLowerCase() === uj.toLowerCase())` |
| legfeljebb N elem, gomb letiltása | `gomb.disabled = t.length >= N` + `if (t.length >= N) return;` |
| darabszám kijelzése | `szamlalo.innerText = t.length` a renderben |
| mező ürítése csak siker esetén | `input.value = ""` az összes `return` után |
| legördülő lista változásakor | `change`; `select.value`, `select.selectedOptions[0]` |
| csúszka mozgatásakor | `input`; `csuszka.value` (string!) |
| méret pixelben | `style.height = v + "px"` |
| osztály feltételtől függően | `classList.toggle("nev", feltetel)` |
| több elemen ugyanaz | `for (const el of querySelectorAll(...))` |
| ellenőrző gomb: üres eset, siker, kudarc | `if (...) { uzenet; return; }`, `toggle("ready", ok)`, template string |
| siker után tiltás, kudarc után szerkeszthető | `for (const v of [...]) v.disabled = ok;` |
| táblázat az adatokból | `tbody.innerHTML = data.map(...).join("")` |
| sor kijelölése kattintásra | `data-id` + `find` + `selected = !selected` |
| összeg: a kijelölteké, ha nincs, az összesé | `filter` + ternary + `reduce` |
| kijelöltek növelése, csökkentése, min. 0 | `filter` + `forEach` + `Math.max(..., 0)` |
| rendezés fejlécre kattintva | `th.dataset.sort` + `sort` + `obj[mezo]` |

### Lista ellenőrzött felvétellel

```js
let elemek = [];

function render(){
    lista.innerHTML = elemek.map(x => `<li>${x}</li>`).join("");
    szamlalo.innerText = elemek.length;
    hozzaad.disabled = elemek.length >= 4;
}

hozzaad.addEventListener("click", () => {
    const uj = input.value.trim();
    if (uj === "") return;                                               // üres
    if (elemek.some(x => x.toLowerCase() === uj.toLowerCase())) return;  // már szerepel
    if (elemek.length >= 4) return;                                      // tele
    elemek.push(uj);
    input.value = "";                                                    // csak siker esetén
    render();
});
```

### Vezérlők: select, csúszka, ellenőrzés

```js
select.addEventListener("change", () => {
    kep.src = select.value;
    kep.alt = select.selectedOptions[0].text;
});

csuszka.addEventListener("input", () => {
    const v = Number(csuszka.value);
    kijelzo.innerText = v;
    for (const el of lapok) {                    // querySelectorAll eredménye
        el.style.width = v * 20 + "px";
        el.classList.toggle("fast", v >= 4);
    }
});

ellenoriz.addEventListener("click", () => {
    if (elemek.length === 0) {                     // üres eset: csak üzenet
        statusz.innerText = "...";
        return;
    }
    const adat = Number(select.selectedOptions[0].dataset.pages);   // option data-* attribútuma
    const szukseges = /* képlet a feladatból */;
    const ok = Number(ido.value) >= szukseges;    // a KEREKÍTETLEN értékkel hasonlíts
    doboz.classList.toggle("ready", ok);
    statusz.innerText = `${ok ? "Sikerüzenet" : "Hibaüzenet"} (${szukseges.toFixed(2)} perc)`;
    for (const v of [csuszka1, csuszka2, select, input, ellenoriz]) v.disabled = ok;
    hozzaad.disabled = ok || elemek.length >= 4;   // a max-N tiltás ne éledjen fel!
});
```

### Interaktív táblázat: kijelölés, összeg, +/−, rendezés

```js
data.forEach(v => v.selected = false);           // segédmező

function render(){
    tbody.innerHTML = data.map(v => `<tr data-id="${v.id}" class="${v.selected ? "selected" : ""}">
        <td>${v.year}</td><td>${v.title}</td><td>${v.views} million</td>
    </tr>`).join("");
    const kij = data.filter(v => v.selected);
    sumSpan.innerText = (kij.length > 0 ? kij : data).reduce((acc, v) => acc + v.views, 0);
}
render();

tbody.addEventListener("click", e => {            // sor kijelölése
    const tr = e.target.closest("tr");
    if (!tr) return;
    const v = data.find(x => x.id === tr.dataset.id);
    v.selected = !v.selected;
    render();
});

function valtoztat(k){                             // k = 1 vagy -1
    const x = k * Number(input.value);
    data.filter(v => v.selected).forEach(v => v.views = Math.max(v.views + x, 0));
    render();
}
btnAdd.addEventListener("click", () => valtoztat(1));
btnSub.addEventListener("click", () => valtoztat(-1));

table.addEventListener("click", e => {            // rendezés fejlécre kattintva
    if (!e.target.matches("th")) return;
    const m = e.target.dataset.sort;               // <th data-sort="year">
    data.sort((a, b) => a[m] > b[m] ? -1 : 1);     // csökkenő
    render();
});
```

## 3. feladat – rács, kattintás, delegálás

A JS építi fel a táblázatot vagy a listát, ezért a kattintásokat a szülőn kell kezelni (delegálás). Két út van: állapot + render (fények, szorzótábla), vagy a meglévő elemek közvetlen mozgatása (könyvek).

| Ha a feladat ezt kéri | Használd |
| N×N mátrix feltöltése számolt értékkel | dupla `for`, vagy `[...Array(n).keys()].map(...)` |
| táblázat egy mátrixból | dupla `map` + `join` |
| üres rács, rows × cols | `"<td></td>".repeat(cols)`, majd `.repeat(rows)` |
| egy cella adott sorban és oszlopban | `table.rows[r].cells[c]` |
| a kattintott cella sora, oszlopa | `td.closest("tr").rowIndex`, `td.cellIndex` |
| elem létrehozása egy cellába | `createElement` + `appendChild` |
| kattintás a generált elemeken | delegálás: `closest`, vagy a kapott `delegate` |
| sor kiemelése egérrel | `mouseover` / `mouseout` + `closest("tr")` |
| legfeljebb egy kijelölt | régi `.selected` levétele, majd `toggle` |
| áthelyezés másik cellába | `appendChild` (átkerül, nem másolódik) |
| üres-e a cella | `!cella.querySelector(".book")`, `!classList.contains("shelf")` |
| két elem adata egyezik-e | `a.dataset.author === b.dataset.author` |
| minden a helyén van-e | `[...querySelectorAll(...)].every(...)` |
| elem a kattintás helyére | `e.offsetX`, `e.offsetY` + `left` / `top` |
| rádiógomb értéke | `form.elements["nev"].value` |
| ciklikusan következő érték | szótár-objektum: `kov[aktualis]` |
| értékek körbeforgatása | `pop` + `unshift` (vagy `shift` + `push`) |
| ismétlés másodpercenként | `setInterval(fv, 1000)`, leállítás: `clearInterval` |

### Mátrix feltöltése és kirajzolása

```js
// N×N szorzótábla (eseménykezelőben)
const n = parseInt(input.value);
if (isNaN(n) || n < 1) return;                 // rossz bemenet
let matrix = [];
for (let i = 0; i < n; i++) {
    matrix[i] = [];
    for (let j = 0; j < n; j++)
        matrix[i][j] = (i + 1) * (j + 1);
}

// ugyanez röviden
const m2 = [...Array(n).keys()].map(i => [...Array(n).keys()].map(j => (i + 1) * (j + 1)));

// rows × cols, minden cella 0  (NE Array(rows).fill([]): az egy közös sor lenne!)
const ures = Array.from({ length: rows }, () => Array(cols).fill(0));

// kirajzolás
table.innerHTML = matrix.map(sor => `<tr>${
    sor.map(c => `<td>${c}</td>`).join("")
}</tr>`).join("");

// kattintott cella → mátrix eleme
const td = e.target.closest("td");
matrix[td.closest("tr").rowIndex][td.cellIndex] *= 2;
```

### Teljes példa: mátrix-táblázat, összeg, nullázás, sorkiemelés

Generáld ki a táblázatot a mátrixból, írd ki a cellák összegét, kattintásra legyen a cella 0 és frissüljön az összeg, az egér alatti sor legyen világoskék.

```js
const matrix = [
    [5, 3, 8],
    [1, 9, 2],
    [7, 4, 6]
];
const table = document.querySelector("table");
const sum = document.querySelector("#sum");

table.innerHTML = matrix.map(row => `<tr>${
    row.map(cell => `<td>${cell}</td>`).join('')
}</tr>`).join('');

function osszegFrissites(){
    const cellak = table.querySelectorAll("td");
    let osszeg = 0;
    for(const cella of cellak){
        osszeg+=Number(cella.innerText);
    }
    sum.innerText=osszeg;
}
osszegFrissites();

table.addEventListener("click", function(e){
    if (e.target.matches("td")) {
        e.target.innerText="0";
    }
    osszegFrissites();
});

delegate(table, "mouseover", "tr", function(){
    this.style.background="lightblue";
});
delegate(table, "mouseout", "tr", function(){
    this.style.background="";
});

function delegate(parent, type, selector, handler) {
  parent.addEventListener(type, function (event) {
    const targetElement = event.target.closest(selector);

    if (this.contains(targetElement)) {
      handler.call(targetElement, event);
    }
  });
}
```

### Delegálás

| Esemény | Mikor | Delegálható |
| `click`, `input`, `change` | kattintás, húzás / gépelés, választás | igen |
| `mouseover` / `mouseout` | egér rá / le | igen |
| `mouseenter` / `mouseleave` | egér rá / le | nem (nem buborékol) |

```js
// ALAP: sima closest, mindig működik
table.addEventListener("click", e => {
    const td = e.target.closest("td");          // matches: csak maga az elem; closest: ősei is
    if (!td) return;
    // ...
});

// SOR KIEMELÉSE
table.addEventListener("mouseover", e => { const tr = e.target.closest("tr"); if (tr) tr.style.backgroundColor = "yellow"; });
table.addEventListener("mouseout",  e => { const tr = e.target.closest("tr"); if (tr) tr.style.backgroundColor = ""; });

// ELŐADÁS delegate: (szülő, ESEMÉNY, szelektor, fv), this = elem → function kell
function delegate(parent, type, selector, handler) {
  parent.addEventListener(type, function (event) {
    const targetElement = event.target.closest(selector);
    if (this.contains(targetElement)) handler.call(targetElement, event);
  });
}
delegate(ul, "click", "li", function(){ this.classList.toggle("done"); });

// ZH KEZDŐCSOMAG delegate: (szülő, SZELEKTOR, esemény, fv), az elem a 2. paraméter
delegate(table, "button.book", "click", (e, gomb) => { /* ... */ });
```

A ZH-n mindig nézd meg, melyik `delegate` van a kezdőkódban; ha bizonytalan vagy, a sima `closest`-es változat is jó.

### Rács generálása és elemek mozgatása

```js
table.innerHTML = `<tr>${"<td></td>".repeat(lib.cols)}</tr>`.repeat(lib.rows);

for (const p of lib.shelves) {
    const cella = table.rows[p.row].cells[p.col];
    cella.classList.add("shelf");
    cella.dataset.author = p.author;
}
for (const b of lib.books) {
    const gomb = document.createElement("button");
    gomb.type = "button";
    gomb.classList.add("book");
    gomb.innerText = b.title;
    gomb.title = `${b.author}: ${b.title}`;
    gomb.dataset.author = b.author;
    table.rows[b.row].cells[b.col].appendChild(gomb);
}

// kijelölés: legfeljebb egy, polcon lévőhöz nem nyúlunk
delegate(table, ".book", "click", (e, gomb) => {
    if (gomb.closest(".shelf")) return;
    const regi = table.querySelector(".book.selected");
    if (regi && regi !== gomb) regi.classList.remove("selected");
    gomb.classList.toggle("selected");
});

// áthelyezés cellára
delegate(table, "td", "click", (e, cella) => {
    if (e.target.closest(".book")) return;           // könyvre kattintás csak kijelöl
    const kijelolt = table.querySelector(".book.selected");
    if (!kijelolt) return;
    if (cella.classList.contains("shelf")) {
        if (cella.dataset.author !== kijelolt.dataset.author) return;
    } else if (cella.querySelector(".book")) return;  // foglalt asztali cella
    cella.appendChild(kijelolt);
    kijelolt.classList.remove("selected");
    if ([...table.querySelectorAll(".book")].every(g => g.closest(".shelf")))
        statusz.innerText = "Minden könyv a helyén!";
});
```

### Kattintás helyére, színek, időzítő

```js
const lights = [];
const kov = { "#ff0000": "#00ff00", "#00ff00": "#0000ff", "#0000ff": "#ffff00", "#ffff00": "#ff0000" };

function render(){
    ul.innerHTML = lights.map(l =>
        `<li style="left: ${l.x}px; top: ${l.y}px; background-color: ${l.c};"></li>`).join("");
}

ul.addEventListener("click", e => {
    if (e.target !== ul) return;                  // meglévő elemre kattintva ne
    const c = form.elements["color"].value;
    lights.push({ x: e.offsetX, y: e.offsetY, c: c });
    form.elements["color"].value = kov[c];        // következő szín bejelölése
    render();
});

function eltol(){                                  // piros-kék-zöld → zöld-piros-kék
    const szinek = lights.map(l => l.c);
    szinek.unshift(szinek.pop());
    lights.forEach((l, i) => l.c = szinek[i]);
    render();
}
gomb.addEventListener("click", () => setInterval(eltol, 1000));
```

## Függelék A: tömb- és stringmetódusok

Az első csoport új értéket ad és az eredetit nem bántja; a második helyben módosítja a tömböt.

```js
// ÚJ ÉRTÉK, az eredeti marad
[1, 2, 3].map(x => x * 2)                 // [2, 4, 6]
[1, 2, 3].filter(x => x > 1)              // [2, 3]
[1, 2, 3].find(x => x > 1)                // 2   (ha nincs: undefined)
[1, 2, 3].some(x => x > 2)                // true
[1, 2, 3].every(x => x > 2)               // false
[1, 2, 3].includes(2)                     // true
[1, 2, 3].reduce((acc, x) => acc + x, 0)  // 6
[[1, 2], [3]].flatMap(x => x)             // [1, 2, 3]
[1, 2, 3, 4].slice(0, 2)                  // [1, 2]   (a vég index nincs benne)
["a", "b"].join(", ")                     // "a, b"
Array.from("abc")                         // ["a", "b", "c"]
[...Array(3).keys()]                      // [0, 1, 2]
t.forEach((x, i) => { ... })              // végigmegy, nem ad vissza semmit; i = index

// HELYBEN MÓDOSÍT
t.push(x);    t.pop();                    // a végére tesz / a végéről kivesz
t.unshift(x); t.shift();                  // az elejére tesz / az elejéről kivesz
t.sort((a, b) => a.v > b.v ? -1 : 1);     // csökkenő (növekvő: 1 : -1)
t = t.filter(x => x !== torlendo);        // „törlés”: a tömb let legyen

// STRING
"  Hamlet ".trim()                        // "Hamlet"
"Hamlet".toLowerCase()                    // "hamlet"
"ABBA - Waterloo".split(" - ")            // ["ABBA", "Waterloo"]
"Love Song".includes("Love")              // true
"Emma".length                             // 4
```

A `querySelectorAll` NodeList-et ad: van `forEach` és `for...of`, de nincs `map`, `filter`, `every`. Előtte: `[...lista]`.

## Függelék B: DOM kiolvasás és módosítás

A `style` nevei camelCase-ek, a méreteknek mértékegység kell; a `dataset` és a `value` mindig stringet ad.

```js
// KIJELÖLÉS
const el = document.querySelector("#id");          // első találat vagy null
const lapok = document.querySelectorAll(".page");  // NodeList (lehet üres)
tabla.querySelector("button")                      // csak a tabla belsejében keres

// SZÖVEG ÉS ÉRTÉK
input.value                  // amit beírtak: STRING
input.value = "";            // mező ürítése
el.innerText = "szöveg";
el.innerHTML = "<b>HTML</b>";

// STÍLUS
el.style.backgroundColor = "yellow";
el.style.height = szam + "px";
el.style.width = `${szam * 20}px`;
el.style.backgroundColor = "";        // vissza az eredetire

// OSZTÁLYOK
el.classList.add("selected");
el.classList.remove("selected");
el.classList.toggle("selected");               // ki-be kapcsol
el.classList.toggle("fast", tempo >= 4);       // rajta van, ha a feltétel igaz
el.classList.contains("shelf")                 // true / false

// ATTRIBÚTUMOK
gomb.disabled = true;                 // letiltás (false: engedélyezés)
img.src = "img/emma.svg";  img.alt = "Jane Austen: Emma";
el.title = "Jane Austen: Emma";       // title attribútum
el.dataset.author                     // data-author="..." kiolvasása
el.dataset.author = "Jane Austen";    // data-author beállítása

// LEGÖRDÜLŐ LISTA (select)
select.value                              // a kiválasztott option value-ja
select.selectedOptions[0].text            // a kiválasztott option szövege
select.selectedOptions[0].dataset.pages   // a kiválasztott option data-pages-e

// RÁDIÓGOMB-CSOPORT (name="color")
form.elements["color"].value                // a bejelölt értéke
form.elements["color"].value = "#ff0000";   // másik bejelölése
document.querySelector('input[name="color"]:checked').value

// CHECKBOX
cb.checked                                  // true / false
```

## Függelék C: Math, kerekítés, időzítő, szótár

```js
Math.floor(Math.random() * t.length)      // véletlen index: 0 … length-1
Math.floor(Math.random() * 100) + 1       // véletlen egész: 1 … 100
Math.max(x - 5, 0)                        // nem mehet 0 alá
Math.min(a, b)                            // a kisebbik
(25.657).toFixed(2)                       // "25.66" (string!)

Number("12")  parseInt("12px")  +"12"     // 12, 12, 12
Number("")                                // 0  (parseInt("") viszont NaN)
isNaN(n)                                  // NaN-e

const id = setInterval(fuggveny, 1000);   // ismétel másodpercenként (zárójel nélkül!)
clearInterval(id);                        // leállítja
setTimeout(fuggveny, 500);                // egyszer, 0,5 s múlva

const kov = { "#ff0000": "#00ff00", "#00ff00": "#ff0000" };   // szótár-objektum
kov[aktualis]                             // a párja
obj[mezoNev]                              // mező változóból: obj["year"] = obj.year
```