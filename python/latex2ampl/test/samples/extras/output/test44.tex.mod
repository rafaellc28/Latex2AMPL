set JOBS;

param n;


var MachineForJob{j in JOBS} integer >= 1, <= n;


s.t. C1 : alldiff{j in JOBS} MachineForJob[j];


