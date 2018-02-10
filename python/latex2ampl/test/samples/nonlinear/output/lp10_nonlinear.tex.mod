set I, := 1..10;

param c{i in I};


var x{k in I} , <= 100, >= -100, := -2.3;


minimize obj: sum{i in I}exp(x[i]) * (c[i] + x[i] - log(sum{k in I}exp(x[k])));

s.t. C1 : exp(x[1]) + 2 * exp(x[2]) + 2 * exp(x[3]) + exp(x[6]) + exp(x[10]) = 2;

s.t. C2 : exp(x[4]) + 2 * exp(x[5]) + exp(x[6]) + exp(x[7]) = 1;

s.t. C3 : exp(x[3]) + exp(x[7]) + exp(x[8]) + 2 * exp(x[9]) + exp(x[10]) = 1;


