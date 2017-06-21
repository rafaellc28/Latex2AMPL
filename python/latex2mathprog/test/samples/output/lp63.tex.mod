set E dimen 2;

set V;

param W{i in V};


var x{i in V} binary;


minimize obj: sum{i in V}W[i] * x[i];

s.t. C1 {(i,j) in E} :
	x[i] + x[j], >= 1;


solve;


data;

set E :=;

set V :=;

param W :=;


end;
