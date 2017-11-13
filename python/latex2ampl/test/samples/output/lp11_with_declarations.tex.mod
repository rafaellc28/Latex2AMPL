set J;

set P{j in J}, in J, default {};

param t{j in J};


var z;

var x{j in J} >= 0;


minimize obj: z;

s.t. C1 {j in J, k in P[j]} :
	x[j] >= x[k] + t[k];

s.t. C2 {j in J} :
	z >= x[j] + t[j];


