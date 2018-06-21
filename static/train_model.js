var timeoutID;
var timeout = 5000;

const AUTH = {
    GO: 'go',
    CAUTION: 'caution',
    STOP: 'stop'
};

function setup()
{
	poller();
}

function poller()
{
    console.log("-----Polling-----");
    makeReq("GET", "/trains/", 200, repopulateTrains);
}

function repopulateTrains(responseText)
{
	console.log("-----Repopulating trains-----");
	var trains = JSON.parse(responseText);
    var trainViewer = document.getElementById("train-viewer");
    var trainDiv, id, name, speed, authority, length, width, height, mass, crew, pass, frontBlock, backBlock;

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
        id.id = "train-id-" + trains[t]['id'];

        trainDiv.id = "train-div-" + trains[t]['id'];

        speed = document.createElement("p");
        speed.innerHTML = "speed: " + trains[t]['speed'];
        speed.id = "train-speed-" + trains[t]['id'];

        authority = document.createElement("p");
        authority.innerHTML = "authority: " + trains[t]['authority'];
        authority.id = "train-authority-" + trains[t]['id'];

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
        crew.id = "train-crew-" + trains[t]['id'];

        pass = document.createElement("p");
        pass.innerHTML = "pass: " + trains[t]['passengerCount'];
        pass.id = "train-pass-" + trains[t]['id'];

        frontBlock = document.createElement("p");
        if(trains[t]['front_block_id'] != 0)
            frontBlock.innerHTML = "front block: " + trains[t]['front_block_id'];
        else
            frontBlock.innerHTML = "front block: yard";
        frontBlock.id = "train-front-" + trains[t]['id'];

        backBlock = document.createElement("p");
        if(trains[t]['back_block_id'] != 0)
            backBlock.innerHTML = "back block: " + trains[t]['back_block_id'];
        else
            backBlock.innerHTML = "back block: yard";
        backBlock.id = "train-back-" + trains[t]['id'];

        trainDiv.appendChild(name);
        trainDiv.appendChild(id);
        trainDiv.appendChild(speed);
        trainDiv.appendChild(authority);
        trainDiv.appendChild(length);
        trainDiv.appendChild(width);
        trainDiv.appendChild(height);
        trainDiv.appendChild(mass);
        trainDiv.appendChild(crew);
        trainDiv.appendChild(pass);
        trainDiv.appendChild(frontBlock);
        trainDiv.appendChild(backBlock);

        trainViewer.appendChild(trainDiv);

        pollBlockMessage(trains[t]['front_block_id']);
	}

	timeoutID = window.setTimeout(poller, timeout);
}

function pollBlockMessage(blockID)
{
    console.log("-----Poll block message-----");
	makeReq("GET", "/messages/" + blockID, 200, populateMessage);
}

function populateMessage(responseText)
{
    console.log("-----Populating message-----");
    var message = JSON.parse(responseText);
    if(message['text'] != null && message['train_id'] != 0)
    {
        var trainDiv = document.getElementById("train-div-" + message['train_id']);
        var msg = document.createElement("p");
        msg.innerHTML = "message: " + message['text'];

        trainDiv.appendChild(msg);

        // Parse message for speed and authority
        var speed = extractSpeed(message['text']);
        var authority = extractAuthority(message['text']);

        updateSpeedAndAuth(speed,authority,message['train_id']);
    }
    else
    {
        timeoutID = window.setTimeout(poller, timeout);
    }
}

function extractSpeed(message)
{
    if(message != null)
    {
        var speed = parseInt(message);
        if(speed != NaN)
            return speed;
        return 0;
    }
    return 0;
}

function extractAuthority(message)
{
    if(message != null)
    {
        var tokens = message.split(",");
        if(tokens.length > 1)
            return tokens[1].toLowerCase();
        return AUTH.STOP;
    }
    return AUTH.STOP;
}

function updateSpeedAndAuth(speed, authority, trainID)
{
    console.log("-----Update speed and authority-----");
    console.log("Speed: " + speed);
    console.log("Authority: " + authority);
    console.log("Train ID: " + trainID);
	var data;
	data = '{"speed":' + speed + ', "authority":"' + authority + '"}';

    makeReq("PUT", "/trains/" + trainID, 201, populateSpeedAndAuth, data);
}

function populateSpeedAndAuth(responseText)
{
    console.log("-----Populating speed and authority-----");
    var train = JSON.parse(responseText);
    var trainDiv = document.getElementById("train-div-" + train['id']);
    var speed = document.getElementById("train-speed-" + train['id']);
    speed.innerHTML = "speed: " + train['speed'];

    var authority = document.getElementById("train-authority-" + train['id']);
    authority.innerHTML = "authority: " + train['authority'];

    if(parseInt(train['speed']) > 0 && (train['authority'] == AUTH.GO || train['authority'] == AUTH.CAUTION))
        moveForward(train['id']);
    else
        timeoutID = window.setTimeout(poller, timeout);
}

function moveForward(trainID)
{
    console.log("-----Move train forward-----");
    var frontText = document.getElementById("train-front-" + trainID).innerHTML.split(": ")[1];
    var front;
    if(frontText == "yard")
        front = 0;
    else
        front = parseInt(frontText);


    var backText = document.getElementById("train-back-" + trainID).innerHTML.split(": ")[1];
    var back;
    if(backText == "yard")
        back = 0;
    else
        back = parseInt(backText);

    console.log("Front: " + front);
    console.log("Back: " + back);

    var frontNext, backNext;

    if(front != back)
    {
        frontNext = front;
        backNext = back + 1;
    }
    else
    {
        frontNext = front + 1;
        backNext = back;
    }

    console.log("FrontNext: " + frontNext);
    console.log("BackNext: " + backNext);

    window.setTimeout(function(){updateTrainLocation(frontNext,backNext,trainID);}, 5000);
}

function updateTrainLocation(front,back,trainID)
{
    console.log("-----Update train location-----");
    console.log("Front: " + front);
    console.log("Back: " + back);
    console.log("Train ID: " + trainID);
    var data;
	data = '{"front_block_id":' + front + ', "back_block_id": ' + back + '}';
    makeReq("PUT", "/trains/" + trainID, 201, populateTrainLocation, data);
}

function populateTrainLocation(responseText)
{
    console.log("-----Populating train location-----");
    var train = JSON.parse(responseText);
    var trainDiv = document.getElementById("train-div-" + train['id']);
    var front = document.getElementById("train-front-" + train['id']);
    front.innerHTML = "front block: " + train['front_block_id'];

    var back = document.getElementById("train-back-" + train['id']);
    back.innerHTML = "back block: " + train['back_block_id'];

    // timeoutID = window.setTimeout(poller, timeout);
}


// setup load event
window.addEventListener("load", setup, true);
