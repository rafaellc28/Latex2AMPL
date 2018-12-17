window.initExamples = function() {
	$.getJSON("/samples/index.json", function(result, status, xhr) {
		if (status == "error" || status == "timeout" || status == "parsererror") {
			alert("Error recovering labels.");
			return;
		}

		samples = result;
		for (i in samples.samples) {
			sample = samples.samples[i];
			li = "<li><a href='#' onclick='javascript:selectExample("+sample.number+","+sample.decl+","+sample.nonlinear+","+sample.constraint+","+sample.network+","+sample.columnwise+","+sample.complement+")'>"+sample.name+"</a></li>";
			$("#examples").append(li);
		}
	});
}

window.selectExample = function(number, decl, nonlinear, constraint, network, columnwise, complement) {
	
	$.getJSON("/samples?number="+number+"&decl="+decl+"&nonlinear="+nonlinear+"&constraint="+constraint+"&network="+network+"&columnwise="+columnwise+"&complement="+complement, function(result, status, xhr) {
		if (status == "error" || status == "timeout" || status == "parsererror") {
			alert("Error recovering sample.");
			return;
		}
		
		$('#collapse2').collapse("show");
		updateDataEditor(result["data"]);
		updateSimpleEditor(result["sample"]);

		initExample(result["sample"]);
	});
}

var initExample = function(sample) {
	var setObj = false;

	var lines = sample.split("\n");

	var c = 0;
	while (lines[c][0] == "%") {
		c++;
	}

	CONSTRAINTS = [];
	$("#objMathInput").val("");
	$("#objMathInput").blur();
	mountConstraints();

	for (i = c; i < lines.length; i++) {
		
		var line = lines[i];

		if (line && line.trim() != "") {
			//var match = /\\text\{\s*([a-zA-Z\s]+)\s*\}/.exec(line);

			var match = /^\s*\\text\{\s*(maximize)\s*\}|(maximize)|\\text\{\s*(maximize):\s*\}|(maximize):/.exec(line);

			if (!match) {
				match = /^\s*\\text\{\s*(minimize)\s*\}|(minimize)|\\text\{\s*(minimize):\s*\}|(minimize):/.exec(line);
			}
			
			if (!match) {
				match = /^\s*\\text\{\s*(subject\sto)\s*\}|\\text\{\s*(subj\.to)\s*\}|\\text\{\s*(s\.t\.)\s*\}|(subject\sto)\s*|(subj\.to)\s*|(s\.t\.)\s*|\\text\{\s*(subject\sto:)\s*\}|\\text\{\s*(subj\.to:)\s*\}|\\text\{\s*(s\.t\.:)\s*\}|(subject\sto:)\s*|(subj\.to:)\s*|(s\.t\.:)\s*/.exec(line);
			}

			if (match) {
				
				if (match[1].trim() == "minimize" || match[1].trim() == "maximize") {
					if (!setObj) {
						setObj = true;

						$("#obj").val(match[1].trim());
						changeObjective(match[1].trim());
						var obj = line.substring(match.index + match[0].length);

						if (obj.endsWith("\\\\")) {
							//console.log(obj);
							obj = obj.substring(0, obj.length-2);
						}

						$("#objMathInput").val(obj);
						$("#objMathInput").blur();
					}

				} else { //if (match[1] == "subject to" || match[1] == "subj.to" || match[1] == "s.t." ||
						   //match[1] == "subject to:" || match[1] == "subj.to:" || match[1] == "s.t.:") {

					var constr = line.substring(match.index + match[0].length);
					if (constr.endsWith("\\\\")) {
						//console.log(constr);
						constr = constr.substring(0, constr.length-2);
					}

					$("#subjMathInput").val(constr);
					//$("#icon-add-constraint").click();
					UpdateSubjectiveMath(undefined, false);
				}

			} else {
				$("#subjMathInput").val(line);
				//$("#icon-add-constraint").click();
				UpdateSubjectiveMath(undefined, false);
			}
		}
	}
	
	UpdateSubjectiveMathOutput(mountConstraintsOutput());
}
