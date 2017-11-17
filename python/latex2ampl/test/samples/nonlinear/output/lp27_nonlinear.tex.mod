param M integer, > 0;

param N integer, > 0;

set I, := 1..N;

set J, := 1..M;

param y{j in J};

param t{j in J}, := 10 * (j - 1);


var x{i in I} , >= -10, <= 10;


minimize obj: sum{j in J}(y[j] - (x[1] + x[2] * exp(-t[j] * x[4]) + x[3] * exp(-t[j] * x[5]))) ^ 2;


