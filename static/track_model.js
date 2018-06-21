import * as trackcontroller from '/track_controller.js';

var timeoutID;
var timeout = 5000;

function setup()
{
	poller();
}

function poller()
{
	makeReq("GET", "/blocks/", 200, repopulate);
}

function getBlock(blockID)
{
    makeReq("GET", "/blocks/" + blockID, 200, getOccupancy);
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

function repopulate(responseText)
{
	console.log("repopulating!");
	var blocks = JSON.parse(responseText);

    for(b in blocks)
    {
        if(blocks[b]["occupancy"])
            document.getElementById("g"+blocks[b]["id"]+"-button").style.backgroundColor = "red";
        else
            document.getElementById("g"+blocks[b]["id"]+"-button").style.backgroundColor = "green";
	}

	timeoutID = window.setTimeout(poller, timeout);
}

// setup load event
window.addEventListener("load", setup, true);
