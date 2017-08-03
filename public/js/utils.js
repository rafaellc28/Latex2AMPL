var Utils = {
	singleEscapes: {
		//'"': '\\"',
		//'\'': '\\\'',
		'\\\\\\$': '\\\\',
		'\b': '\\b',
		'\f': '\\f',
		'\n': '\\n',
		'\r': '\\r',
		'\t': '\\t'
		// `\v` is omitted intentionally, because in IE < 9, '\v' == 'v'.
		// '\v': '\\x0B'
	},

	escapeTex: function(TeX) {
		var res = TeX;
		for (key in this.singleEscapes) {
			res = res.replace(new RegExp(key, 'g'), this.singleEscapes[key]);
		}

		return res;
	}
}