set UNITS;

set SENSORS;

set STREAMS;

param bigM, := 100;

param A{u in UNITS, k in STREAMS}, default 0;

param emax{k in SENSORS}, >= 0;

param s{k in SENSORS}, > 0;

param y{k in SENSORS}, >= 0;


var x{k in STREAMS} >= 0;

var epos{k in STREAMS} >= 0;

var eneg{k in STREAMS} >= 0;

var gerr{k in STREAMS} binary;


minimize obj: sum{k in SENSORS}(epos[k] + eneg[k] + bigM * gerr[k]);

s.t. C1 {i in UNITS} :
	sum{j in STREAMS}A[i,j] * x[j], = 0;

s.t. C2 {k in SENSORS} :
	y[k], = x[s[k]] + epos[k] - eneg[k];

s.t. C3 {k in SENSORS} :
	epos[k], <= emax[k] + bigM * gerr[k];

s.t. C4 {k in SENSORS} :
	eneg[k], <= emax[k] + bigM * gerr[k];


solve;


data;

set UNITS :=;

set SENSORS :=;

set STREAMS :=;

param A :=;

param emax :=;

param s :=;

param y :=;


end;
