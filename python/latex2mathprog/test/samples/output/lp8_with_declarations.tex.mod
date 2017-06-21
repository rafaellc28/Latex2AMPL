set TASKS dimen 2;

set TASKORDER dimen 4, within {TASKS,TASKS};

param dur{(j,m) in TASKS};

set JOBS, := setof {(j,m) in TASKS} j;

set MACHINES, := setof {(j,m) in TASKS} m;

param BigM, := 1 + sum{(j,m) in TASKS}dur[j,m];


var y{(i,m) in TASKS, (j,m) in TASKS : i < j} binary;

var start{(i,m) in TASKS} >= 0;

var makespan >= 0;


minimize obj: BigM * makespan + sum{(j,m) in TASKS}start[j,m];

s.t. C1 {(j,m) in TASKS} :
	start[j,m] + dur[j,m], <= makespan;

s.t. C2 {(k,n,j,m) in TASKORDER} :
	start[k,n] + dur[k,n], <= start[j,m];

s.t. C3 {(i,m) in TASKS, (j,m) in TASKS : i < j} :
	start[i,m] + dur[i,m], <= start[j,m] + BigM * (1 - y[i,m,j]);

s.t. C4 {(i,m) in TASKS, (j,m) in TASKS : i < j} :
	start[j,m] + dur[j,m], <= start[i,m] + BigM * y[i,m,j];


solve;


data;

set TASKS :=;

set TASKORDER :=;

param dur :=;


end;
