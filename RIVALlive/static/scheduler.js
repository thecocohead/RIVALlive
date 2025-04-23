class Match {
    constructor(number, startTime) {
        this.number = number;
        this.startTime = startTime;
    }

}

function previewSchedule(numTeams) {
    //Input
    rounds = Number(document.getElementById("id_rounds").value);
    cycleTime = Number(document.getElementById("id_cycleTime").value);
    startTime = moment(document.getElementById("id_startTime").value);
    //Get number of matches
    numMatches = Math.ceil((rounds * numTeams) / 4)

    let matches = [];
    //Create matches
    for(let i = 1; i <= numMatches ; i++) {
        matchTime = moment(startTime).add(((i - 1) * cycleTime), "m");

        newMatch = new Match(i, matchTime);
        matches.push(newMatch)
    }


    //Display Matches
    var responseDiv = document.getElementById("preview");
    //clear
    responseDiv.innerHTML = "";

    //Show Base information
    header = document.createElement('b');
    header.textContent = `Total Matches: ${numMatches}`;

    responseDiv.appendChild(header);

    //match table
    table = document.createElement('table');
    tbody = document.createElement('tbody');
    table.appendChild(tbody);

    //first row
    row = document.createElement("tr");
    matchHeader = document.createElement("th");
    startTimeHeader = document.createElement("th");

    matchHeader.textContent = "Match";
    startTimeHeader.textContent = "Start Time";

    row.appendChild(matchHeader);
    row.appendChild(startTimeHeader);

    tbody.appendChild(row);

    matches.forEach(item => {
            row = document.createElement("tr");
            number = document.createElement("th");
            startTime = document.createElement("td");
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