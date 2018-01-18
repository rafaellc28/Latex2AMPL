param S;

set E dimen 2;

param T;

param N integer;

param C{(i,j) in E};


var x{(i,j) in E} >= 0;


minimize obj: sum{(i,j) in E}C[i,j] * x[i,j];

s.t. C1 {i in 1..N} :
	sum{(j,i) in E}x[j,i] + (if i = S then 1) = sum{(i,j) in E}x[i,j] + (if i = T then 1);


