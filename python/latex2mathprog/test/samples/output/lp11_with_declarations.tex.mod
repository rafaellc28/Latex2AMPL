set J;

set P{j in J}, in J, default {};

param t{j in J};


var x{j in J} >= 0;

var z;


minimize obj: z;

s.t. C1 {j in J, k in P[j]} :
	x[j], >= x[k] + t[k];

s.t. C2 {j in J} :
	z, >= x[j] + t[j];


solve;


data;

set J :=;

set P[0] :=;

param t :=;


end;
