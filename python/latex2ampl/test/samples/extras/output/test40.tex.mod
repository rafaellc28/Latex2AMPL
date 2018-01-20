param n integer > 0;

set JOBS, := 1..n;

set MACHINES, := 1..n;

param cap{k in MACHINES} integer >= 0;


var Assign{j in JOBS, k in MACHINES} binary;


s.t. C1 {j in JOBS} :
	sum{k in MACHINES}Assign[j,k] = 1;

s.t. C2 {k in MACHINES} :
	sum{j in JOBS}Assign[j,k] <= cap[k];


