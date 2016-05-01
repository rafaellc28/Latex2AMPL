
var express = require('express');
var jsesc = require('jsesc');

var PythonShell = require('python-shell');
var bodyParser = require('body-parser');

var app = express();

app.set('port', (process.env.PORT || 5000));
app.use(express.static('public'));

// instruct the app to use the `bodyParser()` middleware for all routes
app.use(bodyParser());

app.listen(app.get('port'), function() {
	console.log("Node app is running at localhost:" + app.get('port'));
});

app.post('/', function(req, res){
    var str = req.body.latex;


	console.log(str);

	var pyshell = new PythonShell('python/compiler.py');
	
	// sends a message to the Python script via stdin 
	pyshell.send(str);

	response = "";
	
	pyshell.on('message', function (message) {
	  // received a message sent from the Python script (a simple "print" statement) 
	  console.log("Message:\n");
	  console.log(message);
	  response += message + "\n";
	});
	
	// end the input stream and allow the process to exit 
	pyshell.end(function (err) {
	  if (err)  {
	  	console.log(err);
	  }

	  if (!response || response.trim() == "") {
	  	console.log("Ocorreu erro");
	  	//res.send("Ocorreu erro na geração do MathProg, verifique se o Problema de Programação Linear está correto!");
	  	res.send(jsesc(err));
	  } else{
		res.send("<pre>"+response.replace(/(?:\r\n|\r|\n)/g, '<br />')+"</pre>");
	  }

	  console.log('finished');
	  console.log(response);

	});
	
});
