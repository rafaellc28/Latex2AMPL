param C integer;

set N;


var s;

var x{i in 1..C, 1..C, k in N} binary;


s.t. C1 {i in 1..C, j in 1..C} :
	sum{k in N}x[i,j,k] = 1;

s.t. C2 {k in N} :
	sum{i in 1..C, j in 1..C}x[i,j,k] = 1;

s.t. C3 {i in 1..C} :
	sum{j in 1..C, k in N}k * x[i,j,k] = s;

s.t. C4 {j in 1..C} :
	sum{i in 1..C, k in N}k * x[i,j,k] = s;

s.t. C5 : sum{i in 1..C, k in N}k * x[i,i,k] = s;

s.t. C6 : sum{i in 1..C, k in N}k * x[i,C - i + 1,k] = s;


