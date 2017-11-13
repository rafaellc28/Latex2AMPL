param M;

set TASKS, := 1..M;

param saving{d in 1..M, e in 1..M};

set PAIRS dimen 2, := {a in TASKS, b in TASKS : a < b};


var before{a in TASKS, c in TASKS} binary;


maximize obj: sum{(a,b) in PAIRS}(saving[a,b] * before[a,b] + saving[b,a] * (1 - before[a,b]));

s.t. C1 {a in TASKS, b in TASKS, c in TASKS : a < b and a < c and c < b} :
	before[a,b] - before[c,b] - before[a,c] <= 0;

s.t. C2 {a in TASKS, b in TASKS, c in TASKS : a < b and a < c and b < c} :
	before[a,b] + before[b,c] - before[a,c] <= 1;


