//==============Import==============//
//import { module } from "./file.js";

//==============Export==============//
export const array = [1,2,3,4,5]
export default delegate
//export {something, something2};

//==============Delegate==============//
function delegate(parent, type, selector, handler) {
  parent.addEventListener(type, function (event) {
    const targetElement = event.target.closest(selector);
    if (this.contains(targetElement)) handler.call(targetElement, event);
  });
}

//==============Random Integer==============//
function randomInteger(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

//==============Timed orderedy happenings example==============//
function highlightSeries(i = 0) {
  if (series[i]) {
    toggleHighlight(circles[series[i]-1]);
    setTimeout(() => highlightSeries(i+1), 1000);
  } else {
    divOutput.textContent = "Now you go!"
    canGuess = true;
  }
}

//==============Delegate with remover==============//
function delegatePlus(parent, type, selector, handler) {
    const wrap = function (event) {
        const targetElement = event.target.closest(selector);
        if (this.contains(targetElement)) handler.call(targetElement, event);
  }
  parent.addEventListener(type, wrap);
  return function remove(){
    parent.removeEventListener(type, wrap);
  };
}

//==============Filtering==============//
const filteredArray = array.filter(e =>e % 2 === 0);

//==============Sum==============//
array.reduce((s, e) => s + e, 0);

//==============Copy==============//
[1, 2, 3, 4, 5].map((x) => x * 2)  // -> [2, 4, 6, 8, 10]

//==============Shallow copy==============//
const x3 = [1, 2, 3]
const x4 = x3.slice() //either
const x5 = x3.concat()      //or
//These are all seperate arrays

//==============querySelectorAll==============//
const listItems = document.querySelectorAll('ul > li')  // Returns an array-like object, but isn't an array!
const listItemsArray = Array.from(listItems)  //Now you can use array functions

//==============Getting style==============//
const box = document.querySelector("div");
const computedStyle = window.getComputedStyle(box); //This returns the actual set style for the given element, otherwise it would be all empty when queried

//==============getPosition==============//
function getPosition(element) {
   const parent = element.parentNode;
   const children = Array.from(parent.children);

   return children.indexOf(element) + 1;
}

//==============Class==============//
class Tile {
  constructor(x, y) {
    this.x = y;
    this.y = y;
  }

  get coords() {
    return {x, y};
  }

  distance(tile) {
    return Math.sqrt(
      (tile.x - this.x) ** 2 + (tile.y - this.y) ** 2
    );
  }
}

//==============Time related==============//
const timeout = setTimeout(function () { // Run the function after the added ms
  console.log('tick'); }, 1000);
clearTimeout(timeout);  // If the setTimout hasn't run yet, delete it (it won't run then)

const interval = setInterval(function () {       // Run the function multiple times, with the added ms as breaks between the runs
  console.log('tick'); }, 1000);
clearInterval(interval);   // Clears the setInterval (won't run any more)

//==============A full working timer==============//
const timerText = document.querySelector("#info-timer")
let gameStartTime = null
let timeInterval = null

function updateTimer() {
    const elapsedTime = Math.floor((Date.now() - gameStartTime) / 1000)
    const minutes = Math.floor(elapsedTime / 60)
    const seconds = elapsedTime % 60

    timerText.textContent = `${String(minutes).padStart(2, "0")}:` + `${String(seconds).padStart(2, "0")}`
}

function startTimer() {
    if (timeInterval !== null) {
        clearInterval(timeInterval)
    }

    gameStartTime = Date.now()
    timerText.textContent = "00:00"
    timeInterval = setInterval(updateTimer, 1000)
}

function stopTimer() {
    if (timeInterval !== null) {
        clearInterval(timeInterval)
        timeInterval = null
    }
    if (gameStartTime !== null) {
        updateTimer()
    }
}

//==============Local Storage==============//
localStorage.setItem("foo") = 42; //Storing values
localStorage.bar = 42;            //Storing values
const data = [1, 3, 5, 7];
localStorage.setItem('data', JSON.stringify(data)); //Stores a complex data value
const loadedData = JSON.parse(localStorage.getItem('data'));  //loads it

//==============Using remover delegate==============//
const button = document.querySelector("#btn")
const table = document.querySelector("#toDeleg")

const remover = delegatePlus(table, "click", "td", (event) => {
  console.log("smts")
  console.log(event.target)
})

button.addEventListener("click", remover)