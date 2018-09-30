/*
*
*   Simple server to test Events
*
*
*
*/



// First we need to import the HTTP module. This module contains all the logic for dealing with HTTP requests.
var http = require('http');

// We define the port we want to listen to. Logically this has to be the same port than we specified on ngrok.
const PORT=80;

// We create a function which handles any requests and sends a simple response
function handleRequest(request, response){
  // console.log(request);
   let body = '';
    request.on('data', chunk => {
        body += chunk.toString(); // convert Buffer to string
    });
    request.on('end', () => {
        console.log(body);
        request.end('ok');
    });
  response.end('Ngrok is working! -  Path Hit: ' + request.url);
}

// We create the web server object calling the createServer function. Passing our request function onto createServer guarantees the function is called once for every HTTP request that's made against the server
var server = http.createServer(handleRequest);

// Finally we start the server
server.listen(PORT, function(){
  // Callback triggered when server is successfully listening. Hurray!
  console.log("Server listening on: http://localhost:%s", PORT);
});