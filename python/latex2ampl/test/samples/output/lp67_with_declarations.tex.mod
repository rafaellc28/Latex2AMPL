param n integer, > 0;

param s, in {1..n};

set E dimen 2, within {i in 1..n, j in 1..n};

param t, in {1..n};

param c{(i,j) in E};


var x{(i,j) in E} >= 0;


minimize obj: sum{(i,j) in E}c[i,j] * x[i,j];

s.t. C1 {i in 1..n} :
	sum{(j,i) in E}x[j,i] + (if i = s then 1 else 0) = sum{(i,j) in E}x[i,j] + (if i = t then 1 else 0);


