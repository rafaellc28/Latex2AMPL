var editor = null;

CodeMirror.defineSimpleMode("mathprog", {
  // The start state contains the rules that are intially used
  start: [
    // The regex matches the token, the token property contains the type
    {regex: /"(?:[^\\]|\\.)*?(?:"|$)/, token: "string"},
    // Rules are matched in the order in which they appear, so there is
    // no ambiguity between this one and the one above
    {regex: /(?:param|var|maximize|minimize|s.t.|data|end|set|table|subject|to|subj|solve|check|display|for)\b/,
     token: "keyword"},
    {regex: /dimen|default|integer|binary|logical|symbolic|OUT|IN|and|by|cross|diff|div|else|if|in|Infinity|inter|less|mod|not|or|symdiff|then|union|within/, token: "atom"},
    {regex: /sum|prod|min|max/, token: "def"},
    {regex: /printf/, token: "builtin"},
    {regex: /abs|atan|card|ceil|cos|exp|floor|gmtime|length|log|log10|max|min|round|sin|sqrt|str2time|trunc|Irand224|Uniform01|Uniform|Normal01|Normal/, token: "def"},
    {regex: /0x[a-f\d]+|[-+]?(?:\.\d+|\d+\.?\d*)(?:e[-+]?\d+)?/i,
     token: "number"},
    // A next property will cause the mode to move to a different state
	{regex: /\/\*/, token: "comment", next: "comment"},
    {regex: /[-+\/*=<>!]+/, token: "operator"},
    // indent and dedent properties guide autoindentation
    {regex: /[\{\[\(]/, indent: true},
    {regex: /[\}\]\)]/, dedent: true},
    {regex: /[a-z$][\w$]*/, token: "variable"},
  ],
  // The multi-line comment state.
  comment: [
    {regex: /.*?\*\//, token: "comment", next: "start"},
    {regex: /.*/, token: "comment"}
  ],
  // The meta property contains global information about the mode. It
  // can contain properties like lineComment, which are supported by
  // all modes, and also directives like dontIndentStates, which are
  // specific to simple modes.
  meta: {
    dontIndentStates: ["comment"],
  }
});

window.initEditor = function() {
	editor = CodeMirror.fromTextArea(document.getElementById("editor"), {
	    lineNumbers: true,
	    lineWrapping: true,
	    mode: 'mathprog'
	});
	editor.markClean();
}

window.updateEditor = function(data) {
	editor.markClean();
	editor.setValue(data);
	editor.markClean();
}
