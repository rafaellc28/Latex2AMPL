var dictionary = {};
var samples = {};
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
	initDataEditor();
	initSolver();
	initExamples();
	initMathjaxDisplay();

	$("#collapse2").collapse("hide");
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
