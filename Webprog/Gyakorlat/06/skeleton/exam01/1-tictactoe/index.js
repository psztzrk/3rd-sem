const task1 = document.querySelector('#task1');
const task2 = document.querySelector('#task2');
const task3 = document.querySelector('#task3');
const task4 = document.querySelector('#task4');

const game = [
  "XXOO",
  "O OX",
  "OOO ",
];

task1.textContent = game.every((row) => row.length === game[0].length);
const firstRowArray = game[0].split("");
task2.textContent = 
  firstRowArray.every((char) => char === "X") || 
  firstRowArray.every((char) => char === "O");
const gameArray = game.join("").split("");
task3.textContent = 
  `X / O = ${gameArray.filter((char) => char === "X").length} /
  ${gameArray.filter((char) => char === "O").length} `;
task4.textContent = 
  game.findIndex((row) => row.includes("XXX") || 
  row.includes("OOO"));
