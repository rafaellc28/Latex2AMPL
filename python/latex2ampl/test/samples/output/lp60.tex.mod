set E dimen 2;

set V;


var x{i in V} binary;

var k{i in V} >= 1;


minimize obj: sum{i in V}x[i];

s.t. C1 {(i,j) in E} :
	k[j] - k[i] >= 1 - card(V) * (x[i] + x[j]);

s.t. C2 {i in V} :
	k[i] <= card(V);


