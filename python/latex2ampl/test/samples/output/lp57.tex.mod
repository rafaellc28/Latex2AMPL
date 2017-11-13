set E dimen 2;

set V;

param W{(i,j) in E};


var x{i in V} binary;

var t{(i,j) in E} binary;


maximize obj: sum{(i,j) in E}W[i,j] * (x[i] + x[j] - 2 * t[i,j]);

s.t. C1 {(i,j) in E} :
	0 <= x[i] + x[j] - 2 * t[i,j] <= 1;

s.t. C2 {i in V} :
	x[i] >= 0;


