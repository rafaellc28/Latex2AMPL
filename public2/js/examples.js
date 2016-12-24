window.initExamples = function() {
	$.getJSON("/samples/index.json", function(result, status, xhr) {
		if (status == "error" || status == "timeout" || status == "parsererror") {
			alert("Error recovering labels.");
			return;
		}

		samples = result;
		for (i in samples.samples) {
			sample = samples.samples[i];
			li = "<li><a href='#' onclick='javascript:selectExample("+sample.number+")'>"+sample.name+"</a></li>";
			$("#examples").append(li);
		}
	});
}

window.selectExample = function(number) {
	$.getJSON("/samples?number="+number, function(result, status, xhr) {
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

	for (i = c; i < lines.length; i++) {
		
		var line = lines[i];

		if (line && line.trim() != "") {
			var match = /\\text\{\s*([a-zA-Z\s]+)\s*\}/.exec(line);
			//console.log(match);
			if (match) {
				//console.log(match[1]);
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
					$("#icon-add-constraint").click();
				}

			} else {
				$("#subjMathInput").val(line);
				$("#icon-add-constraint").click();
			}
		}
	}

	/*
	var obj = "\\displaystyle\\sum\\limits_{i \\in I,j \\in J}C_{i,j} * x_{i,j}";
	$("#objMathInput").val(obj);
	$("#objMathInput").blur();
	
	// initialize constraints
	var constr = "\\displaystyle\\sum\\limits_{j \\in J}x_{i,j} \\leq A_{i}, i \\in I";
	$("#subjMathInput").val(constr);
	$("#icon-add-constraint").click();
	
	constr = "\\displaystyle\\sum\\limits_{i \\in I}x_{i,j} \\geq B_{j}, j \\in J,";
	$("#subjMathInput").val(constr);
	$("#icon-add-constraint").click();
	
	constr = "x_{i,j} \\in \\mathbb{N}";
	$("#subjMathInput").val(constr);
	$("#icon-add-constraint").click();
	*/
}
