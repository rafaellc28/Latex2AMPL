param m integer, > 0;

param n integer, > 0;

set I, := 1..m;

set J, := 1..n;

param fixcost{i in I, j in J}, >= 0;

param varcost{i in I, j in J}, >= 0;

param demand{j in J}, >= 0;

param supply{i in I}, >= 0;


var y{i in I, j in J} binary;

var x{i in I, j in J} >= 0;


minimize obj: sum{i in I, j in J}varcost[i,j] * x[i,j] + sum{i in I, j in J}fixcost[i,j] * y[i,j];

s.t. C1 {i in I} :
	sum{j in J}x[i,j] = supply[i];

s.t. C2 {j in J} :
	sum{i in I}x[i,j] = demand[j];

s.t. C3 {i in I, j in J} :
	x[i,j] <= min(supply[i],demand[j]) * y[i,j];


