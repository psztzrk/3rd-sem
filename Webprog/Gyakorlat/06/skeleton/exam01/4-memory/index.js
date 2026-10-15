const inputCircleNumber = document.querySelector("#circle-number");
const buttonStart = document.querySelector("#start");
const divContainer = document.querySelector("#container");
const divOutput = document.querySelector("#output");

// Application state

let canGuess = false;
let solution = [];
let series = [];

// ========= Utility functions =========

function delegate(parent, type, selector, handler) {
  parent.addEventListener(type, function (event) {
    const targetElement = event.target.closest(selector);
    if (this.contains(targetElement)) handler.call(targetElement, event);
  });
}

function random(a, b) {
  return Math.floor(Math.random() * (b - a + 1)) + a;
}

function toggleHighlight(node) {
  node.classList.toggle("highlight")
  node.addEventListener("animationend", function (e) {
    node.classList.remove("highlight");
  }, {once: true});
}

// =====================================
let circles = [];
inputCircleNumber.addEventListener("input", (event) => {
  divContainer.innerHTML = "";
  circles = [];
  for (let i = 1; i <= event.target.value; i++) {
    const circle = document.createElement("a");
    circle.classList.add("circle");
    circle.textContent = i;
    divContainer.append(circle);
    circles.push(circle);
  }
})


buttonStart.addEventListener("click", () => {
  series = [];
  for (let i = 1; i <= 7; i++) {
    series.push(random(1, circles.length));
  }
  console.log(series);

  //toggleHighlight(circles[0]);  //1 kört felvillant

  divOutput = "Flashing circles...";
  highlightSeries();
})

function highlightSeries(i = 0){
  if (series[i]) {
    toggleHighlight(circles[series[i] - 1]);
    setTimeout(() => highlightSeries(i + 1), 1000)
  }
  else {
    canGuess = true;
    divOutput = "Now your turn...";
  }
}

delegate(divContainer, "click", "a.cirle", (event) => {
  if(solution.length < series.length){
    solution.push(Number(event.target.textContent));
  }
  if (solution.length === series.length) {
    const haveWon = solution.join("") === series.join("");
    console.log(haveWon);
    divOutput.textContent = haveWon ? "Nice job!" : "Failed!";
  }
  
});