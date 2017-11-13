param N integer;


var x{i in 1..N, j in 1..N} binary;


maximize obj: sum{i in 1..N, j in 1..N}x[i,j];

s.t. C1 {i in 1..N} :
	sum{j in 1..N}x[i,j] <= 1;

s.t. C2 {j in 1..N} :
	sum{i in 1..N}x[i,j] <= 1;

s.t. C3 {k in 2 - N..N - 2} :
	sum{i in 1..N, j in 1..N : i - j = k}x[i,j] <= 1;

s.t. C4 {k in 3..N + N - 1} :
	sum{i in 1..N, j in 1..N : i + j = k}x[i,j] <= 1;


