set E dimen 2;

set V;


var x{i in V} binary;


maximize obj: sum{i in V}x[i];

s.t. C1 {(i,j) in E} :
	x[i] + x[j] <= 1;


