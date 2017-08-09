//
//  Use a closure to hide the local variables from the
//  global namespace
//
var initMathjaxDisplay = function () {
	var TIMEOUT = 120000;

	var QUEUE = MathJax.Hub.queue;  // shorthand for the queue
	var objMath = null, objectiveFunction = null;    // the element jax for the objective math output, and the objectiveFunction it's in

	var subjMath = null, subjectiveFunction = null;    // the element jax for the subjective math output, and the subjectiveFunction it's in

	//
	//  Hide and show the objectiveFunction (so it doesn't flicker as much)
	//
	var hideObjectiveFunction = function () { 
		if (objectiveFunction) objectiveFunction.style.visibility = "hidden";
	};

	var hideSubjectiveFunction = function () {
		if (subjectiveFunction) subjectiveFunction.style.visibility = "hidden";
	};

	var showObjectiveFunction = function () {
		if (objectiveFunction) objectiveFunction.style.visibility = "visible";
	};
	
	var showSubjectiveFunction = function () {
		if (subjectiveFunction) subjectiveFunction.style.visibility = "visible";
	};

	//
	//  Get the element jax when MathJax has produced it.
	//
	QUEUE.Push(function () {
		objMath = MathJax.Hub.getAllJax("objectiveMathOutput")[0];
		objectiveFunction = document.getElementById("objectiveFunction")
		showObjectiveFunction(); // objectiveFunction is initially hidden so the braces don't show

		subjMath = MathJax.Hub.getAllJax("subjectiveMathOutput")[0];
		subjectiveFunction = document.getElementById("subjectiveFunction")
		showSubjectiveFunction(); // subjectiveFunction is initially hidden so the braces don't show
	});

	var getObjMath = function() {
		if (!objMath) {
			objMath = MathJax.Hub.getAllJax("objectiveMathOutput")[0]
		}
	}
	//QUEUE.Push(initExample);

	var queueObj = function(TeX) {
		QUEUE.Push(
		    hideObjectiveFunction,
		    ["Text", objMath, (!TeX || !TeX.trim()) ? "" : "\\displaystyle{"+TeX+"}"],
		    showObjectiveFunction
		);
	}

	//
	//  The onchange event handler that typesets the objMath entered
	//  by the user.  Hide the objectiveFunction, then typeset, then show it again
	//  so we don't see a flash as the objMath is cleared and replaced.
	//
	window.UpdateObjectiveMath = function (TeX) {
		if (!objMath) {
			MathJax.Hub.Typeset(document.getElementById("objectiveMathOutput"), function() {
				getObjMath();
				queueObj(TeX);
			});
			
		} else {
			queueObj(TeX);
		}

		$("div.MathJax_Display").css("text-align", "left");
		$("#objPreviewMathOutput").css("visibility", "hidden");
		$("#objPreviewMathBuffer").css("visibility", "hidden");
		$("#objPreviewMathOutput").css("display", "none");
		$("#objPreviewMathBuffer").css("display", "none");
	}

	var prepareTex = function() {
		var TeX = $("#subjMathInput").val();

		if (!TeX || !TeX.trim()) { return ""; }

		var subjTeXHtmlOld = $("#subjectiveMathInput").html();
		if (!subjTeXHtmlOld) { 
			subjTeXHtmlOld = "";
		}
		
		TeX = Utils.escapeTex(TeX);

		return TeX;
	}
	//
	//  The onchange event handler that typesets the subjMath entered
	//  by the user.  Hide the subjectiveFunction, then typeset, then show it again
	//  so we don't see a flash as the subjMath is cleared and replaced.
	//
	window.UpdateSubjectiveMath = function (event) {
		event.preventDefault();

		var TeX = prepareTex();

		if (!TeX || !TeX.trim()) { return; }

		var keyTeX = getConstraintKey();
		addConstraint(keyTeX, TeX);

		$("#subjectiveMathInput ol").html(mountConstraintsInput());
		$("#subjMathInput").val("");

		UpdateSubjectiveMathOutput(mountConstraintsOutput());

		$("div.MathJax_Display").css("text-align", "left");

	    var popover = $('#subjMathInput').data('bs.popover');
	    popover.options.html = true;
	    popover.options.placement = "bottom";
	    popover.options.content = "";
	    popover.hide();
	}

	var getSubjMath = function() {
		if (!subjMath) {
			subjMath = MathJax.Hub.getAllJax("subjectiveMathOutput")[0]
		}
	}
	//QUEUE.Push(initExample);

	var queueSubj = function(subjTeX) {
		QUEUE.Push(
	    	hideSubjectiveFunction,
	    	["Text", subjMath, (!subjTeX || !subjTeX.trim()) ? "" : "\\displaystyle{"+subjTeX+"}"],
	    	showSubjectiveFunction
		);
	}

	window.UpdateSubjectiveMathOutput = function(subjTeX) {
		if (!subjMath) {
			MathJax.Hub.Typeset(document.getElementById("sujectiveMathOutput"), function() {
				getSubjMath();
				queueSubj(subjTeX);
			});
			
		} else {
			queueSubj(subjTeX);
		}
	}

	window.removeItemInput = function(elem) {
		$(elem).closest("li").remove();
	}

	window.getConstraintKey = function() {
		return CONSTRAINT_KEY++;
	}

	window.findIndexConstraint = function(key) {
		var len = CONSTRAINTS.length;
		for (var i = 0; i < len; i++) {
			if (CONSTRAINTS[i]["key"] == key) {
				return i;
			}
		}

		return -1;
	}

	window.addConstraint = function(key, TeX) {
		CONSTRAINTS.push({"key": key, "tex": TeX});
	}

	window.updateConstraint = function(key, TeX) {
		var idx = findIndexConstraint(key);

		if (idx > -1) {
			CONSTRAINTS[idx]["tex"] = TeX;
		}
	}

	window.removeConstraint = function(key) {
		var idx = findIndexConstraint(key);

		if (idx > -1) {
			CONSTRAINTS.splice(idx, 1);
		}
	}

	window.mountConstraintsOutput = function() {
		var res = "";
		var len = CONSTRAINTS.length;

		for (var i = 0; i < len; i++) {
			res += CONSTRAINTS[i]["tex"] + "\\\\\n";
		}

		var last3 = res.slice(-3);
		if (last3 == "\\\\\n") {
			res = res.substring(0, res.length-3);
		}

		return res;
	}

	window.mountConstraintsInput = function() {
		var res = "";
		var len = CONSTRAINTS.length;
		
		for (var i = 0; i < len; i++) {
			var subjTeXInput = "<li class='list-group-item' id='"+CONSTRAINTS[i]["key"]+"'><div class='alert alert-info fade in'><div class='container-fluid'><div class='row'>"+
				"<div class='col-xs-1'><span class='drag-handle glyphicon glyphicon-move'></span></div>"+
				"<div class='col-xs-9' id='tex'>"+CONSTRAINTS[i]["tex"]+"</div>"+
				"<div class='col-xs-2'><span style='width:35px; float: right;'><a href='#' id='edit' class='alert-link' onclick='javascript: editConstraint(event, this, \""+CONSTRAINTS[i]["key"]+"\");'><i class='glyphicon glyphicon-pencil' aria-hidden='true'></i></a>&nbsp;"+
				"<a href='#' onclick='javascript:removeConstraint(\""+CONSTRAINTS[i]["key"]+"\");removeItemInput(this);UpdateSubjectiveMathOutput(mountConstraintsOutput());' class='close' data-dismiss='alert' aria-label='close'>&times;</a></span></div>"+
				"</div></div></div></li>";
			res += subjTeXInput;
		}

		return res;
	}

	window.editConstraint = function(event, elem, key) {
		event.preventDefault();

		var idx = findIndexConstraint(key);
		$("#subjMathInput").val(CONSTRAINTS[idx]["tex"]);
		$("#subjMathInput").focus();

	    PreviewSubjctiveFunction.Update();

	    $(elem).closest(".alert").removeClass("alert-info");
	    $(elem).closest(".alert").addClass("alert-warning");

	    $("ol.list-constraints").children().each(function( index ) {
	    	$(this).find("#edit").hide();
	    });

	    $("#icon-add-constraint").hide();
	    $("#icon-update-constraint").show();
	    
	    EDITING = key;
	}

	window.updateConstraintMath = function(event) {
		event.preventDefault();
		
		var TeX = prepareTex();

		if (!TeX || !TeX.trim()) { return; }

		updateConstraint(EDITING, TeX);

		$("#subjectiveMathInput ol").html(mountConstraintsInput());
		$("#subjMathInput").val("");
		
		UpdateSubjectiveMathOutput(mountConstraintsOutput());
		
	    $("#icon-add-constraint").show();
	    $("#icon-update-constraint").hide();
	    
	    EDITING = null;
	}

	window.changeObjective = function (textObj) {
		if (textObj == "maximize") {
			$("#objective").html(dictionary["MAXIMIZE"]);
		} else {
			$("#objective").html(dictionary["MINIMIZE"]);
		}
	}

	var processMathOutputLatexEditor = function() {
		var obj = $("#obj").val();
		var objFunc = MathJax.Hub.getAllJax("objectiveMathOutput")[0];
		if (!objFunc["originalText"] || !objFunc["originalText"].trim() || objFunc["originalText"].trim() == "{}") {
			$("#alertObj").html("<div class='alert alert-danger fade in'><a href='#' class='close' data-dismiss='alert' aria-label='close'>&times;</a>"+dictionary["ERROR_OBJ_FUNCTION_EMPTY"]+"</div>");
			return;
		}
		
		var subjFunc = MathJax.Hub.getAllJax("subjectiveMathOutput")[0];
		if (!objFunc["originalText"] || !subjFunc["originalText"].trim() || subjFunc["originalText"].trim() == "{}") {
			$("#alertSubj").html("<div class='alert alert-danger fade in'><a href='#' class='close' data-dismiss='alert' aria-label='close'>&times;</a>"+dictionary["ERROR_SUBJ_FUNCTION_EMPTY"]+"</div>");
			return;
		}

		objFunc = objFunc["originalText"].substring(14, objFunc["originalText"].length-1);
		subjFunc = subjFunc["originalText"].substring(14, subjFunc["originalText"].length-1);

		var data = "\\text{" + obj + " } " + objFunc + "\\\\\n" + "\\text{subject to } " + subjFunc;

		return data;
	}

	window.generateMathProg = function() {
		var data = processMathOutputLatexEditor();

		if (data) {
			showPleaseWait();

			$.post({
				url: "/", 
				data: {latex: data},
				success: function(result, status) {
					updateMathProgEditor(result);
				},
				error: function() {
					alert(dictionary["ERROR_REQUEST"])
				},
				complete: function() {
					hidePleaseWait();
				},
				timeout: TIMEOUT
			});
		}

	}

	window.generateMathProgFromSimpleEditor = function() {
		var idPreview = "mathOutput";
		var preview = document.getElementById(idPreview);
		if (preview.style.visibility == "hidden") {
			idPreview = "mathOutputBuffer";
		}

		var data = MathJax.Hub.getAllJax(idPreview)[0];
		if (!data["originalText"] || !data["originalText"].trim() || data["originalText"].trim() == "{}") {
			$("#alertObj").html("<div class='alert alert-danger fade in'><a href='#' class='close' data-dismiss='alert' aria-label='close'>&times;</a>"+dictionary["ERROR_LP_EMPTY"]+"</div>");
			data = undefined;
		} else {
			data = data["originalText"].substring(14, data["originalText"].length-1);
		}

		if (data) {
			showPleaseWait();

			$.post({
				url: "/", 
				data: {latex: data},
				success: function(result, status) {
					updateMathProgEditor(result);
				},
				error: function() {
					alert(dictionary["ERROR_REQUEST"])
				},
				complete: function() {
					hidePleaseWait();
				},
				timeout: TIMEOUT
			});
		}
	}

	window.copyToSimpleEditor = function() {
		var data = processMathOutputLatexEditor();
		$('#collapse2').collapse("show");
		updateSimpleEditor(data);
	}

	window.copyToDataSection = function() {
		var data;
		var mathProgCode = getValueMathProgEditor();
		var dataCode = getValueDataEditor();

		var idx = mathProgCode.indexOf("data;\n");
		if (idx == -1) {
			idx = mathProgCode.indexOf("end;\n");
		}

		if (idx == -1) {
			data = dataCode;
		} else {
			data = mathProgCode.substring(0, idx);
			data += "data;\n\n" + dataCode + "\n\nend;\n";
		}
		
		$('#collapse2').collapse("show");
		updateMathProgEditor(data);
	}

	window.formatLatexCode = function() {
		var latexCode = getValueSimpleEditor();
		var latexLines = latexCode.split("\n");

		var formattedLatexCode = "";
		var c = 0;
		while (latexLines[c][0] == "%") {
			formattedLatexCode += latexLines[c] + "\n";
			c++;
		}

		formattedLatexCode += "\\begin{equation}\n\\begin{split}\n";

		for (i = c; i < latexLines.length; i++) {
			//console.log(latexLines[i]);
			var line = latexLines[i];

			if (line && line.trim() != "") {
				var match = /^\s*\\text\{\s*maximize\s*\}|maximize|\\text\{\s*maximize:\s*\}|maximize:/.exec(line);

				if (!match) {
					match = /^\s*\\text\{\s*minimize\s*\}|minimize|\\text\{\s*minimize:\s*\}|minimize:/.exec(line);
				}
				
				if (!match) {
					match = /^\s*\\text\{\s*subject\sto\s*\}|\\text\{\s*subj\.to\s*\}|\\text\{\s*s\.t\.\s*\}|subject\sto\s*|subj\.to\s*|s\.t\.\s*|\\text\{\s*subject\sto:\s*\}|\\text\{\s*subj\.to:\s*\}|\\text\{\s*s\.t\.:\s*\}|subject\sto:\s*|subj\.to:\s*|s\.t\.:\s*/.exec(line);
				}
				
				if (match) {
					formattedLatexCode += match + " & " + line.substring(match.index + match[0].length) + "\n";

				} else {

					if (line[0] == "%") {
						formattedLatexCode += line + "\n";
					} else {
						formattedLatexCode += " & " + line + "\n";
					}
					
				}
			}
		}

		formattedLatexCode += "\\end{split}\n\\end{equation}\n";

		updateSimpleEditor(formattedLatexCode);
	}

	var pleaseWaitDiv = $("#pleaseWaitDialog");
    
    var showPleaseWait = function() {
            pleaseWaitDiv.modal();
    };

    var hidePleaseWait = function () {
            pleaseWaitDiv.modal('hide');
    };

	MathJax.Hub.Configured();
};
