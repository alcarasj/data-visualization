const express = require('express');
const path = require("path")
const PORT = 8080;

var server = express();

server.get("/", (req, res) => {
	res.sendFile(path.join(__dirname, 'index.html'));	
});

server.listen(PORT, (error) => {
	if (error) {
		return console.log("Server failed to start.", err);
	}
	console.log("Server listening on port " + PORT + ".");
});
