set I;

set J;

param A{i in I};

param C{i in I, j in J};

param B{j in J};


var x{i in I, j in J} integer >= 0;


minimize obj: sum{i in I, j in J}C[i,j] * x[i,j];

s.t. C1 {i in I} :
	sum{j in J}x[i,j] <= A[i];

s.t. C2 {j in J} :
	sum{i in I}x[i,j] >= B[j];


