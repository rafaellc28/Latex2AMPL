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

	initEditor();
	initSolver();
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
		
	}, 3000);
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

/*var adjustment;

$("ol.list-constraints").sortable({
  group: 'list-constraints',
  handle: 'i.drag-handle',
  cancel: '',
  // animation on drop
  onDrop: function  ($item, container, _super) {
    var $clonedItem = $('<li/>').css({height: 0});
    $item.before($clonedItem);
    $clonedItem.animate({'height': $item.height()});

    $item.animate($clonedItem.position(), function  () {
      $clonedItem.detach();
      _super($item, container);
    });
  },

  // set $item relative to cursor position
  onDragStart: function ($item, container, _super) {
    var offset = $item.offset(),
        pointer = container.rootGroup.pointer;

    adjustment = {
      left: pointer.left - offset.left,
      top: pointer.top - offset.top
    };

    _super($item, container);
  },
  onDrag: function ($item, position) {
    $item.css({
      left: position.left - adjustment.left,
      top: position.top - adjustment.top
    });
  }
});
*/