set I;

set J;

param A{i in I, j in J};

param C{i in I, j in J};

param B{i in I};


var x{i in I, j in J} binary;


minimize obj: sum{i in I, j in J}C[i,j] * x[i,j];

s.t. C1 {j in J} :
	sum{i in I}x[i,j], = 1;

s.t. C2 {i in I} :
	sum{j in J}A[i,j] * x[i,j], <= B[i];


solve;


data;

set I :=;

set J :=;

param A :=;

param C :=;

param B :=;


end;
