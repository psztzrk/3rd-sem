const input = document.querySelectorAll('input');
const button = document.querySelector('button');

const sourceInput = input[0];
const targetOutput = input[1];

button.addEventListener('click', () => {targetOutput.value = sourceInput.value})

/*  tanári megoldás ez volt:
const [from, to] = document.querySelectorAll('input');
const copy = document.querySelector('button');
copy.addEventListener('click', () => to.value = from.value);
*/