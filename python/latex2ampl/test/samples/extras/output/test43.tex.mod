set JOBS;

param n;


var MachineForJob{j2 in JOBS} integer >= 1, <= n;


s.t. C1 {j1 in JOBS, j2 in JOBS : j1 < j2} :
	MachineForJob[j1] != MachineForJob[j2];


