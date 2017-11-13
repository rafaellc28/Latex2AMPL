set PAIRS dimen 2;

set TASKS;

param M;

param Saving{d in 1..M, e in 1..M};


var before{a in TASKS, c in TASKS} binary;


maximize obj: sum{(a,b) in PAIRS}(Saving[a,b] * before[a,b] + Saving[b,a] * (1 - before[a,b]));

s.t. C1 {a in TASKS, b in TASKS, c in TASKS : a < b and a < c and c < b} :
	before[a,b] - before[c,b] - before[a,c] <= 0;

s.t. C2 {a in TASKS, b in TASKS, c in TASKS : a < b and a < c and b < c} :
	before[a,b] + before[b,c] - before[a,c] <= 1;

s.t. C3 {d in 1..M, e in 1..M} :
	Saving[d,e] >= 0;


