const AUTH = {
    GO: 'go',
    CAUTION: 'caution',
    STOP: 'stop'
};

const REQUEST_TYPE = {
    TEST_SWITCH: 0,
    TEST_LIGHT: 1,
    TEST_CROSSING: 2,
    ROUTE_TRAIN: 3,
    GET_OCCUPANCY: 4,
    GET_SWITCH_STATES: 5,
    GET_BROKEN_BLOCKS: 6,
    MAINTENANCE: 7
};

function setup()
{
	poller();
}

function poller()
{
    console.log("-----Polling Track Model-----");
    makeReq("GET", "/ctcrequest/", 200, handleCtcRequest);
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
        case TEST_SWITCH:
            testSwitch();
            break;
        case TEST_LIGHT:
            testLight();
            break;
        case TEST_CROSSING:
            testCrossing();
            break;
        case ROUTE_TRAIN:
            routeTrain();
            break;
        case GET_OCCUPANCY:
            getOccupancy();
            break;
        case GET_SWITCH_STATES:
            getSwitchStates();
            break;
        case GET_BROKEN_BLOCKS:
            getBrokenBlocks();
            break;
        case MAINTENANCE:
            maintenance();
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

}

function getSwitchStates()
{

}

function getBrokenBlocks()
{

}

function maintenance()
{

}

window.addEventListener("load", setup, true);
