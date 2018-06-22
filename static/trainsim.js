function makeReq(method, target, retCode, callback, data)
{
	var httpRequest = new XMLHttpRequest();

	if (!httpRequest)
    {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}

	httpRequest.onreadystatechange = makeHandler(httpRequest, retCode, callback);
	httpRequest.open(method, target);

	if (data)
    {
		// alert(data);
		httpRequest.setRequestHeader('Content-Type', 'application/json');
        httpRequest.setRequestHeader('Authorization', 'token ba910a6d-b27b-4947-8134-e5aa0bd02959');
		httpRequest.send(data);
	}
	else
    {
		httpRequest.send();
	}
}

function makeHandler(httpRequest, retCode, callback)
{
	function handler(){
		if (httpRequest.readyState === XMLHttpRequest.DONE)
        {
			if (httpRequest.status === retCode)
            {
				console.log("received response text:  " + httpRequest.responseText);
                if(callback != null && callback != undefined)
				            callback(httpRequest.responseText);
			}
            else
            {
				alert("There was a problem with the request.  You'll need to refresh the page!");
			}
		}
	}
	return handler;
}
