var timeoutID;
var timeout = 5000;

const AUTH = {
    GO: 'go',
    CAUTION: 'caution',
    STOP: 'stop'
};

const REQUEST_TYPE = {
    TEST_SWITCH: 1,
    TEST_LIGHT: 2,
    TEST_CROSSING: 3,
    ROUTE_TRAIN: 4,
    GET_OCCUPANCY: 5,
    GET_SWITCH_STATES: 6,
    GET_BROKEN_BLOCKS: 7,
    MAINTENANCE: 8
};

function setup()
{
	pollBlocks();
}

function pollBlocks()
{
    console.log("-----Polling Track Model for Blocks-----");
    makeReq("GET", "/blocks/", 200, repopulateBlockList);
}

function pollSwitches()
{
    console.log("-----Polling Track Model for Switches-----");
    makeReq("GET", "/switches/", 200, repopulateSwitchList);
}

function pollCrossings()
{
    console.log("-----Polling Track Model for Crossings-----");
    makeReq("GET", "/crossings/", 200, repopulateCrossingList);
}

// Poll for communication from CTC
function pollCTC()
{
    console.log("-----Polling CTC-----");
    makeReq("GET", "/ctcrequest/", 200, handleCtcRequest);
}

function handleCtcRequest(responseText)
{
    var request = JSON.parse(responseText);
    var type = request['type'];

    switch(type)
    {
        case REQUEST_TYPE.TEST_SWITCH:
            testSwitch();
            break;
        case REQUEST_TYPE.TEST_LIGHT:
            testLight();
            break;
        case REQUEST_TYPE.TEST_CROSSING:
            testCrossing();
            break;
        case REQUEST_TYPE.ROUTE_TRAIN:
            routeTrain();
            break;
        case REQUEST_TYPE.GET_OCCUPANCY:
            getOccupancy();
            break;
        case REQUEST_TYPE.GET_SWITCH_STATES:
            getSwitchStates();
            break;
        case REQUEST_TYPE.GET_BROKEN_BLOCKS:
            getBrokenBlocks();
            break;
        case REQUEST_TYPE.MAINTENANCE:
            maintenance(request['input']);
            break;
        default:
            break;
    }
}

function testSwitch()
{

}


function testLight()
{

}

function testCrossing()
{

}

function routeTrain()
{

}

function getOccupancy()
{
    // makeReq("GET", "/blocks/", 200, updateBlockOccupancyList);
}

function getSwitchStates()
{

}

function getBrokenBlocks()
{

}

function maintenance(input)
{
    var blockID = parseInt(input.split(" ")[0]);
    var state = input.split(" ")[1];
	var data, data2;
    if(state == 0)
    {
        data = '{"occupancy":"' + false + '"}';
        data2 = '{"id": ' + blockID + ', "occupancy":"' + false + '"}';
    }
    else
    {
        data = '{"occupancy":"' + true + '"}';
        data2 = '{"id": ' + blockID + ', "occupancy":"' + true + '"}';
    }

    window.clearTimeout(timeoutID);
    makeReq("PUT", "/block_status/" + blockID, 201, updateBlockOccupancy, data2);
}

function updateBlockOccupancy(responseText)
{
    var block = JSON.parse(responseText);
    var blockID = block['id'];
    var occ = block['occupancy'];
    var data;
    data = '{"occupancy":"' + occ + '"}';

    window.clearTimeout(timeoutID);
    makeReq("PUT", "/blocks/" + blockID, 201, pollBlocks, data);
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
        item.innerHTML = blocks[b]['id'] + ": " + blocks[b]['occupancy'];
        blockList.appendChild(item);
	}

	timeoutID = window.setTimeout(pollSwitches, timeout);
}

function repopulateSwitchList(responseText)
{
	console.log("-----Repopulating switches-----");
	var switches = JSON.parse(responseText);
    var switchList = document.getElementById("switch-list");
    var item;

    while(switchList.hasChildNodes()){
        switchList.removeChild(switchList.childNodes[0]);
    }

    for(s in switches)
    {
        item = document.createElement("li");
        item.innerHTML = switches[s]['id'] + ": " + switches[s]['state'];
        switchList.appendChild(item);
	}

	timeoutID = window.setTimeout(pollCrossings, timeout);
}

function repopulateCrossingList(responseText)
{
	console.log("-----Repopulating crossings-----");
	var crossings = JSON.parse(responseText);
    var crossingList = document.getElementById("crossing-list");
    var item;

    while(crossingList.hasChildNodes()){
        crossingList.removeChild(crossingList.childNodes[0]);
    }

    for(c in crossings)
    {
        item = document.createElement("li");
        item.innerHTML = crossings[c]['id'] + ": " + crossings[c]['state'];
        crossingList.appendChild(item);
	}

	timeoutID = window.setTimeout(pollCTC, timeout);
}

window.addEventListener("load", setup, true);
