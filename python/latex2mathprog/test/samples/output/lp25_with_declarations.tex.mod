param n integer, >= 3;

set V, := 1..n;

set E dimen 2, within V cross V;

param c{(i,j) in E};


var x{(i,j) in E} binary;

var y{(i,j) in E} >= 0;


minimize obj: sum{(i,j) in E}c[i,j] * x[i,j];

s.t. C1 {i in V} :
	sum{(i,j) in E}x[i,j], = 1;

s.t. C2 {j in V} :
	sum{(i,j) in E}x[i,j], = 1;

s.t. C3 {(i,j) in E} :
	y[i,j], <= (n - 1) * x[i,j];

s.t. C4 {i in V} :
	sum{(j,i) in E}y[j,i] + (if i = 1 then n else 0), = sum{(i,j) in E}y[i,j] + 1;


solve;


data;

param n := 0;

set E :=;

param c :=;


end;
