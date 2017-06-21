param Nc;

set E dimen 2;

set V;


var u{c in 1..Nc} binary;

var x{i in V, c in 1..Nc} binary;


minimize obj: sum{c in 1..Nc}u[c];

s.t. C1 {i in V} :
	sum{c in 1..Nc}x[i,c], = 1;

s.t. C2 {(i,j) in E, c in 1..Nc} :
	x[i,c] + x[j,c], <= u[c];


solve;


data;

param Nc := 0;

set E :=;

set V :=;


end;
