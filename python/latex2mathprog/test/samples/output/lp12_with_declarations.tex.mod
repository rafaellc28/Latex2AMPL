param m integer, > 0;

param n integer, > 0;

set J, := 1..n;

set M, := 1..m;

param p{j in J, a in M}, >= 0;

param sigma{j in J, t in 1..m}, in M;

param K, := sum{j in J, a in M}p[j,a];


var x{j in J, a in M} >= 0;

var Y{i in J, j in J, a in M} binary;

var z;


minimize obj: z;

s.t. C1 {j in J, t in 2..m} :
	x[j,sigma[j,t]], >= x[j,sigma[j,t - 1]] + p[j,sigma[j,t - 1]];

s.t. C2 {i in J, j in J, a in M : i <> j} :
	x[i,a], >= x[j,a] + p[j,a] - K * Y[i,j,a];

s.t. C3 {i in J, j in J, a in M : i <> j} :
	x[j,a], >= x[i,a] + p[i,a] - K * (1 - Y[i,j,a]);

s.t. C4 {j in J} :
	z, >= x[j,sigma[j,m]] + p[j,sigma[j,m]];


solve;


data;

param m := 0;

param n := 0;

param p :=;

param sigma :=;


end;
