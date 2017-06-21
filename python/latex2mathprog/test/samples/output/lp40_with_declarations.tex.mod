param n integer, > 0, := 4;

set N, := 1..n ^ 2;


var x{i in 1..n, 1..n, k in N} binary;

var s;


s.t. C1 {i in 1..n, j in 1..n} :
	sum{k in N}x[i,j,k], = 1;

s.t. C2 {k in N} :
	sum{i in 1..n, j in 1..n}x[i,j,k], = 1;

s.t. C3 {i in 1..n} :
	sum{j in 1..n, k in N}k * x[i,j,k], = s;

s.t. C4 {j in 1..n} :
	sum{i in 1..n, k in N}k * x[i,j,k], = s;

s.t. C5  : sum{i in 1..n, k in N}k * x[i,i,k], = s;

s.t. C6  : sum{i in 1..n, k in N}k * x[i,n - i + 1,k], = s;


solve;


end;
