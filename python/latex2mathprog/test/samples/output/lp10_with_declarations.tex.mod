set TASKS, := {'Kitchen','Bathroom','Commons','Trash'};

param T, := 7;

set VOLS, := 1..7;

set WEEKS, := 1..T;

set PAIRS dimen 2, := setof {u in VOLS, v in VOLS : u < v} (u,v);


var x{v in VOLS, t in TASKS, w in WEEKS} binary;

var p{(u,v) in PAIRS, t in TASKS, w in WEEKS} binary;

var z integer;


minimize obj: z;

s.t. C1 {v in VOLS, w in WEEKS} :
	sum{t in TASKS}x[v,t,w], = 1;

s.t. C2 {w in WEEKS} :
	sum{v in VOLS}x[v,'Trash',w], = 1;

s.t. C3 {t in TASKS, w in WEEKS : t <> 'Trash'} :
	sum{v in VOLS}x[v,t,w], = 2;

s.t. C4 {t in TASKS, v in VOLS : t <> 'Trash'} :
	sum{w in WEEKS}x[v,t,w], >= 2;

s.t. C5 {v in VOLS} :
	sum{w in WEEKS}x[v,'Trash',w], <= z;

s.t. C6 {t in TASKS, w in WEEKS, (u,v) in PAIRS} :
	p[u,v,t,w], <= x[u,t,w];

s.t. C7 {t in TASKS, w in WEEKS, (u,v) in PAIRS} :
	p[u,v,t,w], <= x[v,t,w];

s.t. C8 {t in TASKS, w in WEEKS, (u,v) in PAIRS} :
	p[u,v,t,w], >= x[u,t,w] + x[v,t,w] - 1;

s.t. C9 {(u,v) in PAIRS} :
	sum{t in TASKS, w in WEEKS}p[u,v,t,w], >= 1;


solve;


end;
