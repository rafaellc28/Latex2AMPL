set DIGITS;

set LETTERS;


var carry{i in 1..3} binary;

var x{i in LETTERS, d in DIGITS} binary;

var dig{i in LETTERS};


s.t. C1 {i in LETTERS} :
	sum{d in DIGITS}x[i,d] = 1;

s.t. C2 {d in DIGITS} :
	sum{i in LETTERS}x[i,d] <= 1;

s.t. C3 {i in LETTERS} :
	dig[i] = sum{d in DIGITS}d * x[i,d];

s.t. C4 : dig['D'] + dig['E'] = dig['Y'] + 10 * carry[1];

s.t. C5 : dig['N'] + dig['R'] + carry[1] = dig['E'] + 10 * carry[2];

s.t. C6 : dig['E'] + dig['O'] + carry[2] = dig['N'] + 10 * carry[3];

s.t. C7 : dig['S'] + dig['M'] + carry[3] = dig['O'] + 10 * dig['M'];

s.t. C8 : dig['M'] >= 1;

s.t. C9 {i in 1..3} :
	carry[i] >= 0;


