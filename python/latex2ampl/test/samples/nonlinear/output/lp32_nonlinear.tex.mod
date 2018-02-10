set I, := 1..14;

param a{i in I};

param c{i in I};


var x{i in I} >= 0, := 0.01;


minimize obj: sum{i in I}a[i] / x[i];

s.t. C1 : sum{i in I}c[i] * x[i] = 1;

s.t. C2 {i in {1..5}} :
	x[i] <= 0.04;

s.t. C3 {i in {6..14}} :
	x[i] <= 0.03;


