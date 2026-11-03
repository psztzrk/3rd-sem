# 1. Változók, adattípusok, operátorok

## Változók
- let: újra értékadható
- const: nem deklarálható, nem értékadható újra 
- var: újra értékadható, de nem ajánlott használni

pl: 
```js
   let nev = "Anna";
    let kor = 20;
    kor = 21;
    const PI = 3.14; 
// A const objektumok és tömbök tartalma módosítható, csak maga a változó nem kaphat új referenciát.
    const szamok = [1, 2, 3];
    szamok.push(4); // működik
    // szamok = [5, 6]; // hiba
```

## Adattípusok
- String: szöveges adat, pl: "Hello"
- Number: szám, pl: 42, 3.14
- Boolean: logikai érték, pl: true, false
- Object: objektum, pl: {nev: "Anna", kor: 20}
- Array: tömb, pl: [1, 2, 3]
- Null: üres érték, pl: null
- Undefined: nem definiált érték, pl: undefined

## Operátorok
### Aritmetikai operátorok:
    + 
    - 
    * 
    / 
    % 
    ++ 
    --
### Hasonlítási operátorok:
    == 
    != 
    === 
    !== 
    <, > 
    <=, >=

## 