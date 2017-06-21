set TASKS;

param Dur{j in TASKS};

set ARCS dimen 2, within {TASKS cross TASKS};


var Tef{j in TASKS} >= 0;

var Tf >= 0;

var Tlf{j in TASKS} >= 0;

var Tes{j in TASKS} >= 0;

var Tls{j in TASKS} >= 0;

var Tsl{j in TASKS} >= 0;


minimize obj: card(TASKS) * Tf - sum{j in TASKS}Tsl[j];

s.t. C1 {j in TASKS} :
	Tef[j], <= Tf;

s.t. C2 {j in TASKS} :
	Tlf[j], <= Tf;

s.t. C3 {j in TASKS} :
	Tef[j], = Tes[j] + Dur[j];

s.t. C4 {j in TASKS} :
	Tlf[j], = Tls[j] + Dur[j];

s.t. C5 {j in TASKS} :
	Tsl[j], = Tls[j] - Tes[j];

s.t. C6 {(i,j) in ARCS} :
	Tef[i], <= Tes[j];

s.t. C7 {(j,k) in ARCS} :
	Tlf[j], <= Tls[k];


solve;


data;

set TASKS :=;

param Dur :=;

set ARCS :=;


end;
