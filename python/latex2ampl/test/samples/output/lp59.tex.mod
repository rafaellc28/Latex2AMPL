set E dimen 2;

set V;


var x{(i,j) in E} binary;

var k{i in V} >= 1;


minimize obj: sum{(i,j) in E}x[i,j];

s.t. C1 {(i,j) in E} :
	k[j] - k[i] >= 1 - card(V) * x[i,j];

s.t. C2 {i in V} :
	k[i] <= card(V);


