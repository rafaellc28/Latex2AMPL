param m integer, > 0;

param n integer, > 0;

set I, := 1..m;

set J, := 1..n;

param c{i in I, j in J}, >= 0;


var x{i in I, j in J} >= 0;


minimize obj: sum{i in I, j in J}c[i,j] * x[i,j];

s.t. C1 {i in I} :
	sum{j in J}x[i,j] <= 1;

s.t. C2 {j in J} :
	sum{i in I}x[i,j] = 1;


