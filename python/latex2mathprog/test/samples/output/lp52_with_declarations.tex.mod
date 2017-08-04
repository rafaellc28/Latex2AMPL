param n integer, >= 2;

set V, := {1..n};

set E dimen 2, within V cross V;

set EE dimen 2, := setof {(i,j) in E} (i,j) union setof {(i,j) in E} (j,i);

param z{i in V, case in 0..1}, := (if case = 0 then (min{c in 1..z[i,1]}(if not exists{j in V : j < i and (i,j) in EE} z[j,0] = c then c else z[i,1] + 1)) else (if not exists{j in V : j < i} (i,j) in EE then 1 else max{j in V : j < i and (i,j) in EE}z[j,0]));

param nc, := max{i in V}z[i,0];


var u{c in 1..nc} binary;

var x{i in V, c in 1..nc} binary;


minimize obj: sum{c in 1..nc}u[c];

s.t. C1 {i in V} :
	sum{c in 1..nc}x[i,c], = 1;

s.t. C2 {(i,j) in E, c in 1..nc} :
	x[i,c] + x[j,c], <= u[c];


solve;


data;

param n := 0;

set E :=;


end;
