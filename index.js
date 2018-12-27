
var express = require('express');
var i18n = require("i18n");
var PythonShell = require('python-shell');
var bodyParser = require('body-parser');
var jsesc = require('jsesc');
var _ = require('underscore');
var fs = require('fs');
//var jquery = require("jquery");
var Deferred = require('JQDeferred');
var q = require('q');

var baseSamples = "public/samples";

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
app.use(express.static('public'));

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

app.get('/samples', function(req, res) {
	if (req.query.number) {
		var number = req.query.number;
		var decl = req.query.decl;
		var nonlinear = req.query.nonlinear;
		var constraint = req.query.constraint;
		var network = req.query.network;
		var columnwise = req.query.columnwise;
		var complement = req.query.complement;
		
		result = {}
		
		var name = number
		
		if (nonlinear == "true") {
			name += "_nonlinear";
			
		} else if (nonlinear == "false") {
			name += "_linear";
		}
		
		if (constraint == "true") {
			name += "_constraint";
		}
		
		if (network == "true") {
			name += "_network";
		}

		if (columnwise == "true") {
			name += "_columnwise";
		}
		
		if (complement == "true") {
			name += "_complement";
		}

		if (piecewise == "true") {
			name += "_piecewise";
		}

		if (decl == "true") {
			name += "_with_declarations";
		}
		
		var sample = baseSamples+"/lp"+name+".tex.equation";
		var dataSample = baseSamples+"/data/lp"+name+".tex.dat";
		
		var d = Deferred();
		
		fs.readFile(sample, "utf8", function(err, data){
		    if (err) data = "";
		    result["sample"] = data;
		    
			fs.readFile(dataSample, "utf8", function(err, data){
			    if (err) data = "";
			    result["data"] = data;
			    
			    d.resolve(result);
			});
		});
		
		q.when(d).done(function(result) {
			res.send(result);
		});
		
	} else {
		res.send({});
	}
});


app.post('/', function(req, res) {

    var str = req.body.latex;

	var pyshell = new PythonShell('python/latex2ampl/compiler.py');
	
	// sends a message to the Python script via stdin 
	pyshell.send(str);

	response = "";
	
	pyshell.on('message', function (message) {
	  // received a message sent from the Python script (a simple "print" statement) 
	  response += message + "\n";
	});
	
	// end the input stream and allow the process to exit 
	pyshell.end(function (err) {
	  if (!response || response.trim() == "") {
	  	res.send(jsesc(err));
	  } else{
		res.send(response);
	  }
	});
	
});
