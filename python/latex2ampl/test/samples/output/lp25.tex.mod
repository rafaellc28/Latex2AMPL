set V;

set E dimen 2;

param N integer;

param C{(i,j) in E};


var y{(i,j) in E} >= 0;

var x{(i,j) in E} binary;


minimize obj: sum{(i,j) in E}C[i,j] * x[i,j];

s.t. C1 {i in V} :
	sum{(i,j) in E}x[i,j] = 1;

s.t. C2 {j in V} :
	sum{(i,j) in E}x[i,j] = 1;

s.t. C3 {(i,j) in E} :
	y[i,j] <= (N - 1) * x[i,j];

s.t. C4 {i in V} :
	sum{(j,i) in E}y[j,i] + (if i = 1 then N else 0) = sum{(i,j) in E}y[i,j] + 1;


