param n integer, > 0;

param log2n, := log(n) / log(2);

param k, := floor(log2n);

param a{j in 1..n}, := 2 ^ (k + n + 1) + 2 ^ (k + n + 1 - j) + 1;

param b, := 0.5 * floor(sum{j in 1..n}a[j]);


var x{j in 1..n} binary;


maximize obj: sum{j in 1..n}a[j] * x[j];

s.t. C1  : sum{j in 1..n}a[j] * x[j], <= b;


solve;


data;

param n := 0;


end;
