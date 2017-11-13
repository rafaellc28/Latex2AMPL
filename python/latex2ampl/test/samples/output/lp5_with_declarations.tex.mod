set C;

set N;

param Data{c in C, n in {"price","weight"} union N};

param Allowance{n in N};


var x{c in C} >= 0;


minimize obj: sum{c in C}x[c];

s.t. C1 {n in N} :
	sum{c in C}Data[c,n] * x[c] >= Allowance[n];


