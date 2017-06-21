param n integer, >= 0;

set V, := 1..n;

set E dimen 2, within V cross V, default setof {i in V, j in V : i <> j and Uniform(0, 1) <= 0.15} (i,j);


var k{i in V} >= 1, <= card(V);

var x{(i,j) in E} binary;


minimize obj: sum{(i,j) in E}x[i,j];

s.t. C1 {(i,j) in E} :
	k[j] - k[i], >= 1 - card(V) * x[i,j];


solve;


data;

param n := 0;

set E :=;


end;
