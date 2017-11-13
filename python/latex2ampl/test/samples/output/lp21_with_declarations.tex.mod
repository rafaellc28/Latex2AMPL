set I;

set J;

param f;

param a{i in I};

param b{j in J};

param d{i in I, j in J};

param c{i in I, j in J}, := f * d[i,j] / 1000;


var x{i in I, j in J} >= 0;


minimize obj: sum{i in I, j in J}c[i,j] * x[i,j];

s.t. C1 {i in I} :
	sum{j in J}x[i,j] <= a[i];

s.t. C2 {j in J} :
	sum{i in I}x[i,j] >= b[j];


