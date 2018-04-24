/**
* Here is an example of the communication with the server using HTTP request.
* It is not meant to be used outside testing purposes.
*/

var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;
var IP_ADDRESSE = "128.179.178.60";
var PORT = "3000";

function sendReq(){

    var request = new XMLHttpRequest();
    // Use post instead of GET for now.
    request.open('POST', 'http://'+IP_ADDRESSE+':'+PORT, true);
    request.setRequestHeader("Content-type", "application/json");

    
    request.onload = () => {
      if (request.status >= 200 && request.status < 400) {
        // Success!
        const res = JSON.parse(request.responseText);
        console.log(res);
      } else {
        // We reached our target server, but it returned an error
        console.log("Error on server side.")
      }
    };

    request.onerror = () => {
      // There was a connection error of some sort
        console.log("Error on communication.");
    };

    request.send(JSON.stringify({"year":1996}));
}   

sendReq();