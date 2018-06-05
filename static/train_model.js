var timeoutID;
var timeout = 5000;

function setup()
{
	poller();
}

function poller()
{
    makeReq("GET", "/trains/", 200, repopulateTrains);
}

function pollBlockMessage(blockID)
{
	makeReq("GET", "/messages/" + blockID, 200, updateMessage);
}

function repopulateTrains(responseText)
{
	console.log("repopulating!");
	var trains = JSON.parse(responseText);
    var trainViewer = document.getElementById("train-viewer");
    var trainDiv, id, name, speed, length, width, height, mass, crew, pass, msg;

    while(trainViewer.hasChildNodes())
    {
        trainViewer.removeChild(trainViewer.childNodes[0]);
    }

    for(t in trains)
    {
        trainDiv = document.createElement("div");

        name = document.createElement("h2");
        name.innerHTML = trains[t]['name'];

        id = document.createElement("p");
        id.innerHTML = "id: " + trains[t]['id'];

        speed = document.createElement("p");
        speed.innerHTML = "speed: " + trains[t]['speed'];

        length = document.createElement("p");
        length.innerHTML = "length: " + trains[t]['length'];

        width = document.createElement("p");
        width.innerHTML = "width: " + trains[t]['width'];

        height = document.createElement("p");
        height.innerHTML = "height: " + trains[t]['height'];

        mass = document.createElement("p");
        mass.innerHTML = "mass: " + trains[t]['mass'];

        crew = document.createElement("p");
        crew.innerHTML = "crew: " + trains[t]['crewCount'];

        pass = document.createElement("p");
        pass.innerHTML = "pass: " + trains[t]['passengerCount'];

        msg = document.createElement("p");
        console.log(trains[t]['front_block_id']);
        console.log(trains[t]['front_block_id'].message);
        if(trains[t]['front_block_id'] != null)
            msg.innerHTML = "message: " + trains[t]['front_block_id'].message;
        else
            msg.innerHTML = "message: ";

        trainDiv.appendChild(name);
        trainDiv.appendChild(id);
        trainDiv.appendChild(speed);
        trainDiv.appendChild(length);
        trainDiv.appendChild(width);
        trainDiv.appendChild(height);
        trainDiv.appendChild(mass);
        trainDiv.appendChild(crew);
        trainDiv.appendChild(pass);
        trainDiv.appendChild(msg);

        trainViewer.appendChild(trainDiv);
	}

	// timeoutID = window.setTimeout(poller, timeout);
}

// setup load event
window.addEventListener("load", setup, true);
