param n integer > 0;

set JOBS, := 1..n;

set MACHINES, := 1..n;

param cap{k in MACHINES} integer >= 0;


var MachineForJob{j in JOBS} integer >= 1, <= n;


s.t. C1 {k in MACHINES} :
	count {j in JOBS} (MachineForJob[j] = k) <= cap[k];


