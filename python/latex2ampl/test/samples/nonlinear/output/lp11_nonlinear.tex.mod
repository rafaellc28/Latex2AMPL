set I, := 1..10;

param c{i in I};


var x{k in I} >= 1e-6, := .1;


minimize obj: sum{i in I}x[i] * (c[i] + log(x[i] / (sum{k in I}x[k])));

s.t. C1  : x[1] + 2 * x[2] + 2 * x[3] + x[6] + x[10] = 2;

s.t. C2  : x[4] + 2 * x[5] + x[6] + x[7] = 1;

s.t. C3  : x[3] + x[7] + x[8] + 2 * x[9] + x[10] = 1.5;


