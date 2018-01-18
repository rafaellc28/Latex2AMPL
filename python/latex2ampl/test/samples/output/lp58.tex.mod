param S symbolic;

set E dimen 2;

param T symbolic;

set V;

param A{(i,j) in E};


var flow >= 0;

var x{(i,j) in E} >= 0;


maximize obj: flow;

s.t. C1 {i in V} :
	sum{(j,i) in E}x[j,i] + (if i = S then flow) = sum{(i,j) in E}x[i,j] + (if i = T then flow);

s.t. C2 {(i,j) in E} :
	x[i,j] <= A[i,j];


