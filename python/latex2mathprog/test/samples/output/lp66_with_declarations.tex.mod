param m integer, > 0;

param n integer, > 0;

set C{i in 1..m};


var x{j in 1..n} binary;

var y{i in 1..m} binary;


minimize obj: sum{i in 1..m}y[i];

s.t. C1 {i in 1..m} :
	sum{j in C[i]}(if j > 0 then x[j] else (1 - x[-j])) + y[i], >= 1;


solve;


data;

param m := 0;

param n := 0;

set C[0] :=;


end;
