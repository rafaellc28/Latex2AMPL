set I;

set J;

param Fixcost{i in I, j in J};

param Demand{j in J};

param Varcost{i in I, j in J};

param Supply{i in I};


var y{i in I, j in J} binary;

var x{i in I, j in J} >= 0;


minimize obj: sum{i in I, j in J}Varcost[i,j] * x[i,j] + sum{i in I, j in J}Fixcost[i,j] * y[i,j];

s.t. C1 {i in I} :
	sum{j in J}x[i,j] = Supply[i];

s.t. C2 {j in J} :
	sum{i in I}x[i,j] = Demand[j];

s.t. C3 {i in I, j in J} :
	x[i,j] <= min(Supply[i],Demand[j]) * y[i,j];


