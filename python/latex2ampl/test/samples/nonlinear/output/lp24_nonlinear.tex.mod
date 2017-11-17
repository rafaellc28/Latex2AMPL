set I, := {1..11};

param a{i in I};

param c{i in I};

param b{i in I}, := 1 / c[i];


var x{1..4} , <= 0.42, >= 0, := .42;


minimize obj: sum{i in I}(a[i] - x[1] * (b[i] ^ 2 + b[i] * x[2]) / (b[i] ^ 2 + b[i] * x[3] + x[4])) ^ 2;


