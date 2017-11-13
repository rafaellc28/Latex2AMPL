param f1, > 0;

param f2, > 0;

param f3, > 0;

param f4, > 0;

param ncomp integer > 0;

param neq integer > 0;

set I, := {1..ncomp};

set J, := {1..neq};

param f, := f1 * f2 * f3 / f4;

param a{i in I}, > 0;

param c{i in I}, > 0;

param b{i in I}, > 0;

param d{i in I}, > 0;


var x{i in I} >= 0;


minimize obj: sum{i in I}a[i] * x[i];

s.t. C1 {i in J} :
	x[i + neq] / (b[i + neq] * sum{j in J}x[j + neq] / b[j + neq]) = c[i] * x[i] / (40 * b[i] * sum{j in J}x[j] / b[j]);

s.t. C2  : sum{i in I}x[i] = 1;

s.t. C3  : sum{i in J}x[i] / d[i] + f * sum{i in J}x[i + neq] / b[i + neq] = 1.671;


