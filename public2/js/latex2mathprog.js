var dictionary = {};
var CONSTRAINT_KEY = 0;
var CONSTRAINTS = [];
var EDITING = null;

var init = function() {
	$('[data-toggle="popover"]').popover();
	$("ol.list-constraints").sortable({
		handle: '.drag-handle',
		cancel: '',
		update: function(event, ui) {

			CONSTRAINTS_AUX = [];
			$( "ol.list-constraints" ).children().each(function( index ) {
				var idx = findIndexConstraint(this.id);
				CONSTRAINTS_AUX.push({"key": CONSTRAINTS[idx]["key"], "tex": CONSTRAINTS[idx]["tex"]});
			});

			CONSTRAINTS = CONSTRAINTS_AUX;
			CONSTRAINTS_AUX = [];
			UpdateSubjectiveMathOutput(mountConstraintsOutput());
		}
	});

	PreviewObjctiveFunction.Init();
	PreviewSubjctiveFunction.Init();
	PreviewSimpleEditor.Init();

	initMathProgEditor();
	initSimpleEditor();
	initSolver();

	$("#collapse2").collapse("hide");
}

var initExample = function() {
	setTimeout(function() {

		// initialize objective function
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
		
	}, 5000);
}

var loadUser = function() {
	var lang = $.url().param('lang');
	if (!lang) lang = "en";
	
	$.getJSON("/json?lang="+lang, function(result, status, xhr) {
		if (status == "error" || status == "timeout" || status == "parsererror") {
			alert("Error recovering labels.");
			return;
		}

		dictionary = result;

		var template = $('#template').html();
		Mustache.parse(template);   // optional, speeds up future uses
		
		var rendered = Mustache.render(template, dictionary);
		$('#target').html(rendered);

		init();
	});

}
