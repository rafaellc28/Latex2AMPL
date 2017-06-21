set JOBS;

param BigM;

param Dur{k in JOBS};

param Due{k in JOBS};

param Rel{k in JOBS};


var start{j in JOBS} >= 0;

var pastdue{k in JOBS} >= 0;

var y{j in JOBS, k in JOBS} binary;


minimize obj: sum{k in JOBS}pastdue[k];

s.t. C1 {k in JOBS} :
	start[k], >= Rel[k];

s.t. C2 {k in JOBS} :
	start[k] + Dur[k], <= Due[k] + pastdue[k];

s.t. C3 {j in JOBS, k in JOBS : j < k} :
	start[j] + Dur[j], <= start[k] + BigM * (1 - y[j,k]);

s.t. C4 {j in JOBS, k in JOBS : j < k} :
	start[k] + Dur[k], <= start[j] + BigM * y[j,k];


solve;


data;

set JOBS :=;

param BigM := 0;

param Dur :=;

param Due :=;

param Rel :=;


end;
