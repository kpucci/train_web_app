var timeoutID;
var timeout = 5000;

function setup()
{
	pollTrains();
}

function poller()
{
	makeReq("GET", "/blocks/", 200, repopulate);
}

function createTrain()
{
    var trainName = document.getElementById("train-name").value;
    var data = '{"name":"' + trainName + '"}';
    makeReq("POST", "/trains/", 201, pollTrains, data);
    document.getElementById("train-name").value = "";
}

function pollTrains()
{
    makeReq("GET", "/trains/", 200, repopulateTrains);
}

function makeCtcRequest(type,input)
{
    var data;
	data = '{"type":"' + type + '","input":"' + input + '"}';

    makeReq("PUT", "/ctcrequest/", 201, poller, data);
}

function getOccupancy(responseText)
{
    var block = JSON.parse(responseText);
    var blockID = block["id"];
    var occupancy = block["occupancy"];

	var data;
	data = '{"occupancy":"' + !occupancy + '"}';

    makeReq("PUT", "/blocks/" + blockID, 201, poller, data);
}

function repopulateTrains(responseText)
{
	console.log("repopulating!");
	var trains = JSON.parse(responseText);
    var trainList = document.getElementById("train-list");
    var item;

    while(trainList.hasChildNodes()){
        trainList.removeChild(trainList.childNodes[0]);
    }

    for(t in trains)
    {
        item = document.createElement("li");
        item.innerHTML = trains[t]['name'];
        trainList.appendChild(item);
	}

	// timeoutID = window.setTimeout(poller, timeout);
}

// setup load event
window.addEventListener("load", setup, true);
