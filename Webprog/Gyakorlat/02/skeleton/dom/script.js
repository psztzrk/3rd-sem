/*
 * 1. feladat
 * Írd ki egymás alá 5x, egyre növekvő betűméretekkel a "Hello világ!" szöveget!
 *
 * Gondolatmenet:
 * - hozz létre egy szöveget (és mentsd konstansba),
 * - tedd a "létrehozást" egy ciklusba,
 * - minden iteráció végén állítsd be a szöveg méretét
 */

for (let i = 1; i <= 5; i++) {
  const p = document.createElement("p");
  p.textContent = "Hello világ!";
  p.style.fontSize = 1 + i * 0.25 + "em";
  document.body.appendChild(p);
}

/*
 * 2. feladat
 * Készíts egy táblázat segítségével egy sakktáblát!
 * (8 x 8-as pálya, bal felső mező fehér)
 *
 * Gondolatmenet:
 * - hozz létre egy táblázatot, abban 8 sort, majd azokban 8-8 cellát
 * - használd az indexek összegének kettővel való oszthatóságát
 *   a cellaháttér színezéséhez
 * - távolítsd a cellák közötti alapértelmezett margókat
 *   és állíts be a táblázatnak egy szegélyt
 */

const table = document.createElement("table");
for (let i = 1; i <= 8; i++) {
  const row = document.createElement("tr");
  for (let j = 1; j <= 8; j++) {
    const cell = document.createElement("td");
    cell.style.backgroundColor = (i + j) % 2 ? "black" : "white";
    cell.style.width = "2em";
    cell.style.height = "2em";
    row.appendChild(cell);
  }
  table.style.borderSpacing = 0;
  table.style.border = "1px solid black";
  table.appendChild(row);
}
document.body.appendChild(table);
