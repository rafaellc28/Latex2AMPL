set TASKS dimen 2;

set TASKORDER dimen 4;

param BigM;

param Dur{(j,m) in TASKS};


var start{(i,m) in TASKS} >= 0;

var makespan >= 0;

var y{(i,m) in TASKS, (j,m) in TASKS : i < j} binary;


minimize obj: BigM * makespan + sum{(j,m) in TASKS}start[j,m];

s.t. C1 {(j,m) in TASKS} :
	start[j,m] + Dur[j,m], <= makespan;

s.t. C2 {(k,n,j,m) in TASKORDER} :
	start[k,n] + Dur[k,n], <= start[j,m];

s.t. C3 {(i,m) in TASKS, (j,m) in TASKS : i < j} :
	start[i,m] + Dur[i,m], <= start[j,m] + BigM * (1 - y[i,m,j]);

s.t. C4 {(i,m) in TASKS, (j,m) in TASKS : i < j} :
	start[j,m] + Dur[j,m], <= start[i,m] + BigM * y[i,m,j];


solve;


data;

set TASKS :=;

set TASKORDER :=;

param BigM := 0;

param Dur :=;


end;
