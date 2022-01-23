const path = require("path");
const DataStatistics = require(path.join(__dirname,'DataStatistics.js'));
const http = require('http');
const WebSocketServer = require('websocket').server;


const deviceID = "_3a3d8794ce3bc2e62cb9f5799b8039c765fe3b9a"    // Unique identifier for a Quest device. Hardcoded for
                                                                // dev version, doesn't work for other Quest devices as is!
var MongoClient = require('mongodb').MongoClient;           
var url = "mongodb://localhost:27017/data_test";                // DB URL for dev purposes. Needs to be changed for another user or for production
const dbClient = new MongoClient(url);                          // Get reference to the MongoDB database

// =============================== CREATE HTTP SERVER AND ESTABLISH WEBSOCKET AND LISTENERS ===============================

const server = http.createServer();
var clients = [];

// Handles HTTP requests POST & PUT
// Basically the requests the Quest device makes
server.on('request', (request, response) => {
    const { headers } = request;
    console.log(headers)
    
    if (request.method == 'POST' || request.method == 'PUT'){   // If server gets a post/put call, it assumes it's from the Quest device
        console.log(request.method+" request");                 // and calls a function to save the sent data
        var body =  '';
        request.on('data', function (data){
            body+=data;
        });
        request.on('end', function() {
            response.writeHead(200, {'Content-Type': 'text/html'})
            response.end('put received')
            handleDataSetFromQuestRevised(body)
        })
    }
});

const port = 3210;
server.listen(port);
console.log(`Listening on ${port}`)

const wsServer = new WebSocketServer({
    httpServer: server
});

wsServer.on('connect', function(connection){
    console.log("Client connected");
});
   
// Listener for websocket client requests (python client)
// Saves websocket connection to clients[]
wsServer.on('request', function(request) {
    const connection = request.accept(null, request.origin);
    clients.push(connection);
    connection.on('message', function(message) {
        const msg = message.utf8Data;
        console.log('Received Message:', msg);

        if (msg == 'RequestDataList' ){                                 // Request if list of all recorded data sets
            updateClientListTestAsync(connection).catch(console.dir);
        }
        if (msg.includes('RequestDataMs')){                             // Request of a certain data set by milliseconds from 1.1.1970
            respondToDataRequestMs(connection, msg)
        }
    });

    connection.on('close', function(reasonCode, description) {
        console.log('Client has disconnected.');
    });
});

// Some boilerplate code for authorizing websocket connection from HTTP calls
// Not implemented
server.on('upgrade', function upgrade(request, socket, head) {
    // This function is not defined on purpose. Implement it with your own logic.
    console.log("ws");
    // authenticate(request, (err, client) => {
    //   if (err || !client) {
    //     socket.write('HTTP/1.1 401 Unauthorized\r\n\r\n');
    //     socket.destroy();
    //     return;
    //   }

    //   wss.handleUpgrade(request, socket, head, function done(ws) {
    //     wss.emit('connection', ws, request, client);
    //   });
    // });
});
      

// =============================== END OF HTTP & WEBSOCKET LISTENERS ===============================

// ===============================      Data and response logics     ===============================


// handleDataSetFromQuestRevised()
//
// Function for handling received data from Quest
// Calls some data-analytics for the data
// and calls the save for of data and the analysis to the database
const handleDataSetFromQuestRevised = (data) => {
    var jsondata = JSON.parse(data);
    var dataAnal = new DataStatistics(jsondata);
    var stats = dataAnal.getStatistics();
    jsondata["statistics"] = stats;

    pushDataIntoDatabase(jsondata);

    if (clients.length != 0){
        updateClientListTestAsync();                            // if the server has clients connected,
    } else{                                                     // update the client about the new data
        console.log("No connections");
    }
}

// removeAllDocumentsFromCollection() 
// param: (Quest) unique device ID (as string)
// Function to delete everything from the database
// !! Only used on developement purposes. To be deleted !!
function removeAllDocumentsFromCollection(collection){
    MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        var dbo = db.db("data_test");
        dbo.collection(collection).deleteMany({});
        console.log("Deleted all items from collection " + collection);
    }); 

}

// pushDataIntoDatabase()
// param: Object (JSON)
//
// Function to push received data and it's analysis to DB
const pushDataIntoDatabase = (dataObject) => {
    var device_id = "_"+dataObject.deviceID
    console.log(device_id);
    MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        var dbo = db.db("data_test");
        dbo.collection(device_id).insertOne(dataObject, function(err, res) {
        if (err) throw err;
        console.log("1 document inserted");
        db.close();
        });
    }); 
};
  
// updateClientListTestAsync()
// param: client connection
//
// Function to get all recorded data sets from DB
// and send a list of times (milliseconds from 1.1.1970) of each record
// to the client
//
// TODO-
// Doesn't catch if db is down (or other exceptions)?
// deviceID is hardcoded
async function updateClientListTestAsync(requestClient = clients[0]) {
    try {
        await dbClient.connect();
        const database = dbClient.db("data_test");
        const col = database.collection(deviceID);                          // try to find a collection by deviceID from database


        const cursor = col.find();
        if ((await cursor.count()) === 0) {
        console.log("No documents found!");
        }

        var listOfItems = []
        await cursor.forEach(item => listOfItems.push(item.time));          // get time for each record found
    } finally {
        if (listOfItems != null){
            var strList = stringifyList(listOfItems);                       // get string form of list of records' times
            console.log("sending: "+strList);
            requestClient.sendUTF(strList)                                  // send the list
        }
        
        await dbClient.close();
    }
}

// Function to return a "stringified" array
// The string begins with "listresult"
// and subsequent items are seperated by a comma (",")
const stringifyList = (array) => {
    var list = "listresult";
    for (var i = 0; i < array.length; i++){
        list += array[i];
        list += ','
    }
    list = list.substring(0, list.length-1);
    list += "";
    return list;
}

// respondToDataRequestMs()
// Searches the database with an unique (Quest) deviceID
// with a time (milliseconds from 1.1.1970) to find recorded data
// matching said deviceID and time. Responds with found data.
// Function assumes the client can't request a data for a time that
// isn't in the DB.
//
// !! Device id hardcoded. Doesn't work as is for other Quest devices!!
async function respondToDataRequestMs(client, msg){
    var device_id = deviceID;
    const msRequest = msg.split(" ")[1];
    console.log("Sending data to client, request " + msRequest)

    try {
        await dbClient.connect();
        const database = dbClient.db("data_test");
        const col = database.collection(device_id);                         // find matching deviceID from DB
        const query = { time: msRequest };
        const result = await col.findOne(query);                            // find matching time (ms from 1.1.1970) from DB
        sendDataByMs(client, result);                                       // respond found with data
    } finally {
        await dbClient.close();
    }
}

// Function to send data to a client in string-form
// The string begins with "dataresultMS"
const sendDataByMs = (client, data) => {
    stringdata = JSON.stringify(data)
    stringdata = "dataresultMS"+stringdata
    client.sendUTF(stringdata)
};

// =============================================================================================
