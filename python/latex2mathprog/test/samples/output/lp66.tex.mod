param M integer;

param N integer;

set C{i in 1..M};


var y{i in 1..M} binary;

var x{j in 1..N} binary;


minimize obj: sum{i in 1..M}y[i];

s.t. C1 {i in 1..M} :
	sum{j in C[i]}(if j > 0 then x[j] else (1 - x[-j])) + y[i], >= 1;

s.t. C2 {j in 1..N} :
	x[j], >= 0;


solve;


data;

param M := 0;

param N := 0;

set C[0] :=;


end;
