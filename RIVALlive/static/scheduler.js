class Match {
    constructor(number, startTime) {
        this.number = number;
        this.startTime = startTime;
    }

}

function previewSchedule() {
    //Input
    const teams = parseInt(document.getElementById("numTeams").innerText);
    let rounds = parseInt(document.getElementById("id_rounds").value);
    const cycleTime = parseInt(document.getElementById("id_cycleTime").value);
    const startTime = moment(document.getElementById("id_startTime").value);
    //Check Data


    //Get number of matches
    let numMatches = Math.ceil((rounds * teams) / 4)

    if(isNaN(numMatches)) {
        return;
    }

    let matches = [];
    //Create matches
    for(let i = 1; i <= numMatches ; i++) {
        matchTime = moment(startTime).add(((i - 1) * cycleTime), "m");

        newMatch = new Match(i, matchTime);
        matches.push(newMatch)
    }


    //Display Matches
    let responseDiv = document.getElementById("preview");
    //clear
    responseDiv.innerHTML = "";

    //Show Base information
    let header = document.createElement('b');
    header.textContent = `Total Matches: ${numMatches}`;

    responseDiv.appendChild(header);

    //match table
    let table = document.createElement('table');
    let tbody = document.createElement('tbody');
    table.appendChild(tbody);

    //first row
    let row = document.createElement("tr");
    let matchHeader = document.createElement("th");
    let startTimeHeader = document.createElement("th");

    matchHeader.textContent = "Match";
    startTimeHeader.textContent = "Start Time";

    row.appendChild(matchHeader);
    row.appendChild(startTimeHeader);

    tbody.appendChild(row);

    matches.forEach(item => {
            let row = document.createElement("tr");
            let number = document.createElement("th");
            let startTime = document.createElement("td");
            number.textContent = `Q${item.number}`;
            startTime.textContent = item.startTime.format("ddd hh:mm:ss a");

            row.appendChild(number);
            row.appendChild(startTime);

            tbody.appendChild(row);

        }
    );

    responseDiv.appendChild(table);

    //Add "Run Scheduler" button
    let runSchedulerForm = document.createElement("FORM");
    runSchedulerForm.name = "Run Scheduler";
    runSchedulerForm.method = "POST";


}