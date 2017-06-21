set I;

set J;

param C{i in I, j in J};


var x{i in I, j in J} >= 0;


minimize obj: sum{i in I, j in J}C[i,j] * x[i,j];

s.t. C1 {i in I} :
	sum{j in J}x[i,j], <= 1;

s.t. C2 {j in J} :
	sum{i in I}x[i,j], = 1;


solve;


data;

set I :=;

set J :=;

param C :=;


end;
