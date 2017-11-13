param n integer, > 0;

set V, := 1..n;

set E dimen 2, within V cross V;


var x{i in V} binary;


maximize obj: sum{i in V}x[i];

s.t. C1 {(i,j) in E} :
	x[i] + x[j] <= 1;


