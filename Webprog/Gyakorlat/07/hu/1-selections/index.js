const taskA = document.querySelector("#taskA")
const taskB = document.querySelector("#taskB")
const taskC = document.querySelector("#taskC")
const taskD = document.querySelector("#taskD")
const taskE = document.querySelector("#taskE")

taskA.textContent = participants.filter(p => p.nation === "CHE").length;

taskB.textContent = participants.some(p => p.nation === "HUN");

taskC.textContent = participants.find((p) => p.type ==="band" && p.name.split(" ").length >= 3).name;

const uniqueNations = [];
for (const p of participants) {
    if (!uniqueNations.includes(nations[p.nation])) 
        {
            uniqueNations.push(nations[p.nation]);
        }
}
//taskD.textContent = participants.map(p => p.nation).map((c) => nations[c]);   --> ez lenne az ismétléses
//taskD.textContent = uniqueNations;
taskD.textContent = uniqueNations.join(", ");

const max = {nation: null, count: -Infinity};
for (const nation of uniqueNations) 
{
    const nationCount = participants.filter((p) => p.nation === nation).length;
    if (nationCount > max.count)
    {
        max.nation = nation;
        max.count = nationCount;
    }
}
taskE.textContent = nations[max.nation];