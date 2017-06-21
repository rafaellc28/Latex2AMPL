param m integer, > 0;

param n integer, > 0;

set I, := 1..m;

set J, := 1..n;

param a{i in I, j in J}, >= 0;

param c{i in I, j in J}, >= 0;

param b{i in I}, >= 0;


var x{i in I, j in J} binary;


minimize obj: sum{i in I, j in J}c[i,j] * x[i,j];

s.t. C1 {j in J} :
	sum{i in I}x[i,j], = 1;

s.t. C2 {i in I} :
	sum{j in J}a[i,j] * x[i,j], <= b[i];


solve;


data;

param m := 0;

param n := 0;

param a :=;

param c :=;

param b :=;


end;
