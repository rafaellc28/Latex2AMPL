param n integer, > 0, := 8;


var x{i in 1..n, j in 1..n} binary;


maximize obj: sum{i in 1..n, j in 1..n}x[i,j];

s.t. C1 {i in 1..n} :
	sum{j in 1..n}x[i,j] <= 1;

s.t. C2 {j in 1..n} :
	sum{i in 1..n}x[i,j] <= 1;

s.t. C3 {k in 2 - n..n - 2} :
	sum{i in 1..n, j in 1..n : i - j = k}x[i,j] <= 1;

s.t. C4 {k in 3..n + n - 1} :
	sum{i in 1..n, j in 1..n : i + j = k}x[i,j] <= 1;


