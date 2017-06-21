set I;

param C;

set J;

param W{i in I};


var used{j in J} binary;

var x{i in I, j in J} binary;


minimize obj: sum{j in J}used[j];

s.t. C1 {i in I} :
	sum{j in J}x[i,j], = 1;

s.t. C2 {j in J} :
	sum{i in I}W[i] * x[i,j], <= C * used[j];


solve;


data;

set I :=;

param C := 0;

set J :=;

param W :=;


end;
