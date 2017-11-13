set E dimen 2;

set V, := (setof {(i,j) in E} i) union (setof {(i,j) in E} j);

param w{i in V}, >= 0, := 1;


var x{i in V} binary;


minimize obj: sum{i in V}w[i] * x[i];

s.t. C1 {(i,j) in E} :
	x[i] + x[j] >= 1;


