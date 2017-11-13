param b, >= 0;

param n integer, > 0;

set U, := 0..2 ^ n - 1;

set N, := 1..n;

param a{j in N}, >= 0;

param x{i in U, j in N}, := (i div 2 ^ (j - 1)) mod 2;

set D, := setof {i in U : sum{j in N}a[j] * x[i,j] <= b} i;


var beta integer >= 0;

var alfa{j in N} integer >= 0;


minimize obj: sum{j in N}alfa[j] + beta;

s.t. C1 {i in D} :
	sum{j in N}alfa[j] * x[i,j] <= beta;

s.t. C2 {i in U diff D} :
	sum{j in N}alfa[j] * x[i,j] >= beta + 1;


