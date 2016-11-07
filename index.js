
var express = require('express');
var i18n = require("i18n");
var PythonShell = require('python-shell');
var bodyParser = require('body-parser');
var jsesc = require('jsesc');
var _ = require('underscore');


i18n.configure({
    directory: __dirname + '/locales'
});


var app = express();

//app.configure(function() {
	
//});

app.use(i18n.init);

// register helper as a locals function wrapped as mustache expects
app.use(function (req, res, next) {
    // mustache helper
    res.locals.__ = function () {
      return function (text, render) {
        return i18n.__.apply(req, arguments);
      };
    };

    next();
});

app.set('port', (process.env.PORT || 5000));
app.use(express.static('public2'));

// instruct the app to use the `bodyParser()` middleware for all routes
app.use(bodyParser.urlencoded({ extended: true }));

app.listen(app.get('port'), function() {
	//console.log("Node app is running at localhost:" + app.get('port'));
});

app.get('/json', function(req, res) {
	if (req.query.lang) {
		var catalog = req.getCatalog(req.query.lang);
		if (catalog && _.size(catalog) > 0) {
			res.send(catalog);
		}
	} else {
		res.send({});
	}
});

app.post('/', function(req, res) {

    var str = req.body.latex;

	//console.log(str);

	var pyshell = new PythonShell('python/v2/compiler.py');
	
	// sends a message to the Python script via stdin 
	pyshell.send(str);

	response = "";
	
	pyshell.on('message', function (message) {
	  // received a message sent from the Python script (a simple "print" statement) 
	  //console.log("Message:\n");
	  //console.log(message);
	  response += message + "\n";
	});
	
	// end the input stream and allow the process to exit 
	pyshell.end(function (err) {
	  if (err)  {
	  	//console.log(err);
	  }

	  if (!response || response.trim() == "") {
	  	//console.log("Ocorreu erro");
	  	//res.send("Ocorreu erro na geração do MathProg, verifique se o Problema de Programação Linear está correto!");
	  	res.send(jsesc(err));
	  } else{
		//res.send(response.replace(/(?:\r\n|\r|\n)/g, '<br />'));
		res.send(response);
	  }

	  //console.log('finished');
	  //console.log(response);

	});
	
});
