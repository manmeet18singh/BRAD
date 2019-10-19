// Express setup
var express = require('express');
var app = express();

var path = require('path');
var port = 8080;

var fs = require('fs');
var shell = require('shelljs');
var ps = require('python-shell');

app.use(express.static(path.join(__dirname, "static")));

app.get("/", function (req, res) {
    res.sendFile(path.join(__dirname, "index.html"))
});

var bodyParser = require('body-parser');
app.use(bodyParser({ 'limit': '500mb' }));
app.use(bodyParser.urlencoded({ extended: true }));

app.post('/getPrediction', (req, res) => {
    var json = req.body;

    var vector = "";

    for(var value in json) {
        vector = vector + String(json[value]) + " ";
    }

    fs.writeFileSync('../brad/temp.txt', vector);
    var result = shell.exec('python3 ../brad/brad.py', {silent: true});
    console.log(result.stdout);
    var output = result.stdout;

    var jsonToSend = {'output': output};
    res.send(JSON.stringify(jsonToSend));
});

app.listen(port, () => {
    console.log("Server listening on port " + port);
});
