console.log("Hello World! :)")

function convertToC(f)
{
    return (f - 32) * 5/9;
}

function convertToF(c){
    return c / (5/9) + 32;
}

function triangleTrueFalse(a, b, c){
    /*
    let result = (a + b > c) && (a + c > b) && (b + c > a)
    ? true
    : false
    return result; */
    return (a + b > c) && (a + c > b) && (b + c > a);
}

function lnko(a, b){
    if (a < b) {
        [a,b] = [b,a];
    }
    let maradek = a % b;
    while (maradek > 0) {
        a = b;
        b = maradek;
        maradek = a % b;
    }

    lnko = b;
    return lnko; 
}

function evenOdd() {
    let numbers = [-1, 2, 3, -4, 5, 6, 7, 8, 9, 10]
        
    return numbers.find(a => a < 0) % 2 === 3
    ? "páros" : "páratlan";
}

function average() {
    let numbers = [-1, 2, 3, -4, 5, 6, 7, 8, 9, 10];
    let elems = numbers.filter(a => a > 2 || a < -2);
    numbers.reduce((acc, curr) => acc + curr, 0) / elems.length;
}