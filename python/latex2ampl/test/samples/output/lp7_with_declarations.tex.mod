set JOBS;

param dur{k in JOBS};

param due{k in JOBS};

param rel{k in JOBS}, default 0;

param bigM, := (max{k in JOBS}rel[k]) + sum{k in JOBS}dur[k];


var y{j in JOBS, k in JOBS} binary;

var start{k in JOBS} >= 0;

var pastdue{k in JOBS} >= 0;


minimize obj: sum{k in JOBS}pastdue[k];

s.t. C1 {k in JOBS} :
	start[k] >= rel[k];

s.t. C2 {k in JOBS} :
	start[k] + dur[k] <= due[k] + pastdue[k];

s.t. C3 {j in JOBS, k in JOBS : j < k} :
	start[j] + dur[j] <= start[k] + bigM * (1 - y[j,k]);

s.t. C4 {j in JOBS, k in JOBS : j < k} :
	start[k] + dur[k] <= start[j] + bigM * y[j,k];


