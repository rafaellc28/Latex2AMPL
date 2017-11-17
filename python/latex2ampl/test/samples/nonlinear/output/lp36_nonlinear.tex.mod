set K;

param M integer, > 0;

param N integer, > 0;

set I, := 1..N;

set J, := 1..M;

param b{j in K}, >= 0;

param a{i in I, j in J}, <= 1,>= 0;

param c{i in I}, <= 0;

param u{j in J}, >= 0;


var x{i in I, j in J} integer >= 0;


minimize obj: sum{j in J}u[j] * (prod{i in I}a[i,j] ^ x[i,j] - 1);

s.t. C1 {j in K} :
	sum{i in I}x[i,j] >= b[j];

s.t. C2 {i in I} :
	-sum{j in J}x[i,j] >= c[i];


