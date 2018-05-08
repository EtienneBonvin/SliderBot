/**
* Nodejs server for SliderBot.
*/

const express = require('express');
const app = express();
var fs = require('fs');

var response = "File not found";

app.post('/', function(req, res){
    // Use post for now.
    console.log('Post request received: ');

    res.writeHead(200, { 'Content-Type': 'text/plain' });
    req.on('data', function (chunk) {
        var buffer = JSON.stringify(chunk);
        var data = JSON.parse(getData(buffer));
    
        console.log('GOT DATA : '+data);
        var year = data.year;
        console.log('Requested year : '+year);
        
        var parsed = JSON.parse(fs.readFileSync('maps/'+year+'.json', 'utf8'));
        console.log(parsed);
        response = JSON.stringify(parsed);
        console.log(response);
        res.end(JSON.stringify({"data":response}));
    });
    
});

app.get('/', function(req, res){
    // GET not available.
    console.log('Get request received: ');
    
    res.writeHead(200, {'Content-Type': 'text/plain'});
    
    console.log(req);
    
    res.end(JSON.stringify({"data": 0}));
});

app.listen(3000, () => {
    console.log('Server listening on port 3000!');
});

function getData(buffer){
    var array = buffer.substr(buffer.indexOf("data")+7, buffer.length);
    var final = array.substr(0, array.indexOf(']'));

    var ascii = final.split(',');

    var dec = "";

    for(var i = 0; i < ascii.length; i++){
        dec += String.fromCharCode(parseInt(ascii[i]));
    }
    return dec;
}