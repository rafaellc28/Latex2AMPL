param m integer, > 0;

param n integer, > 0;

set C{i in 1..m};


var y{i in 1..m} binary;

var x{j in 1..n} binary;


minimize obj: sum{i in 1..m}y[i];

s.t. C1 {i in 1..m} :
	sum{j in C[i]}(if j > 0 then x[j] else (1 - x[-j])) + y[i] >= 1;


