function delegate(parent, type, selector, handler) {
  parent.addEventListener(type, function (event) {
    const targetElement = event.target.closest(selector);
    if (this.contains(targetElement)) handler.call(targetElement, event);
  });
}

const form = document.querySelector("form");
const divContainer = document.querySelector(".container");
const labels = Array.from(divContainer.querySelectorAll("label"))

const inputs = Array.from(form.querySelectorAll("input"));
const consumptions = inputs.map((input) => Number(input.dataset.consumption));
const M = consumptions.reduce((acc, curr) => acc + curr, 0);
console.log(M);


delegate(form, "input", "input", () => {
const currentConsumptions = inputs.map(
  (input) => Number(input.value) / 
  Number(input.max) * 
  Number(input.dataset.consumption));
console.log(currentConsumptions);})

currentConsumptions.forEach((ci, index) => {
  const label = labels(index);
  label.style.width= `${ci / M[index] *100}%`
});
