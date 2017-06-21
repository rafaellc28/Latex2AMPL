set U;

set D;

set N;

param X{i in U, j in N};


var alfa{j in N} integer >= 0;

var beta integer >= 0;


minimize obj: sum{j in N}alfa[j] + beta;

s.t. C1 {i in D} :
	sum{j in N}alfa[j] * X[i,j], <= beta;

s.t. C2 {i in U diff D} :
	sum{j in N}alfa[j] * X[i,j], >= beta + 1;

s.t. C3 {i in U, j in N} :
	X[i,j], >= 0;


solve;


data;

set U :=;

set D :=;

set N :=;

param X :=;


end;
