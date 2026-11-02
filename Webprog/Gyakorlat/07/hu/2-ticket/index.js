const seatingTable = document.querySelector("#seating")
const rowNum = 10
const colNum = 14

//                    0.   1.   2.   3.
const sectorCosts = [250, 350, 200, 100]
let seatsTaken = [0, 0, 0, 0]

function updateTable() 
{
    seatsTaken.forEach((s, i) => 
    {
        document.querySelector(`#sector-${i}-amount`).textContent = seatsTaken[i];
        document.querySelector(`#sector-${i}-total`).textContent = seatsTaken[i] * sectorCosts[i];
    });
    
}
sectorCosts.forEach((c, i) => { document.querySelector(`#sector-${i}-Cost`).textContent = c });

document.querySelector("#add-standing").addEventListener("click", () => {
    seatsTaken[0]++;
    document.querySelector("#sector-0-amount").textContent = seatsTaken[0];
    updateTable();
});

document.querySelector("#sub-standing").addEventListener("click", () => {
    seatsTaken[0]--;
    document.querySelector("#sector-0-amount").textContent = seatsTaken[0];
    updateTable();
});

for (let i = 0; i < rowNum; i++) {
    const row = document.createElement("tr");
    for (let j = 0; j < colNum; j++) 
        {
            const col = document.createElement("td");
            col.classList.add("seat");
            if(i < 3)
            {
                col.classList.add("sector-1");
            }
            else if(i < 6)
            {
                col.classList.add("sector-2");
            }
            else
            {
                col.classList.add("sector-3");
            }
            row.appendChild(col);
            
        }
        
    seatingTable.appendChild(row);
}


function delegate(parent, type, selector, handler) {
  parent.addEventListener(type, function (event) {
    const targetElement = event.target.closest(selector);
    if (this.contains(targetElement)) handler.call(targetElement, event);
  });
}


delegate(seatingTable, "click", "td.seat", (event) => {
    event.target.classList.toggle("selected") ? 1 : -1;
    [event.target.dataset.sector] += seatCount;
});