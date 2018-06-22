var timeoutID;
var timeout = 5000;

function setup()
{
	pollBlocks();
}

function pollBlocks()
{
    makeReq("GET", "/block_status/", 200, repopulateBlockList);
}

function createTrain()
{
    var trainName = document.getElementById("train-name").value;
    var data = '{"name":"' + trainName + '"}';
    window.clearTimeout(timeoutID);
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

    window.clearTimeout(timeoutID);
    makeReq("PUT", "/ctcrequest/", 201, pollTrains, data);
}

function requestMaintenance()
{
    var blockId = document.getElementById("request-maintenance").value;
    makeCtcRequest(8,blockId + " " + 1);
}

function liftMaintenance()
{
    var blockId = document.getElementById("lift-maintenance").value;
    makeCtcRequest(8,blockId + " " + 0);
}

function testSwitch()
{
    var blockId = document.getElementById("test-switch").value;
    makeCtcRequest(1,blockId);
}

function testLight()
{
    var blockId = document.getElementById("test-light").value;
    makeCtcRequest(2,blockId);
}

function testCrossing()
{
    var blockId = document.getElementById("test-crossing").value;
    makeCtcRequest(3,blockId);
}

function routeTrain()
{
    var trainId = document.getElementById("route-train-id").value;
    var trainDest = document.getElementById("route-train-dest").value;
    makeCtcRequest(4,trainId + " " + trainDest);
}

function requestOccupancy()
{
    makeCtcRequest(5);
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

	timeoutID = window.setTimeout(pollBlocks, timeout);
}

function repopulateBlockList(responseText)
{
	console.log("-----Repopulating blocks-----");
	var blocks = JSON.parse(responseText);
    var blockList = document.getElementById("block-list");
    var item;

    while(blockList.hasChildNodes()){
        blockList.removeChild(blockList.childNodes[0]);
    }

    for(b in blocks)
    {
        item = document.createElement("li");
        item.innerHTML = blocks[b]['id'] + ": " + blocks[b]['occupancy'] + ", " + blocks[b]['maintenance'] + ", " + blocks[b]['broken'];
        blockList.appendChild(item);
	}

	timeoutID = window.setTimeout(pollTrains, timeout);
}

// setup load event
window.addEventListener("load", setup, true);
