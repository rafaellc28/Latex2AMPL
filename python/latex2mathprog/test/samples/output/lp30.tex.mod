set UNITS;

set SENSORS;

set STREAMS;

param BigM;

param A{i in UNITS, j in STREAMS};

param Emax{k in SENSORS};

param S{k in SENSORS};

param Y{k in SENSORS};


var gerr{k in SENSORS} binary;

var epos{k in SENSORS} >= 0;

var eneg{k in SENSORS} >= 0;

var x{j in STREAMS} >= 0;


minimize obj: sum{k in SENSORS}(epos[k] + eneg[k] + BigM * gerr[k]);

s.t. C1 {i in UNITS} :
	sum{j in STREAMS}A[i,j] * x[j], = 0;

s.t. C2 {k in SENSORS} :
	Y[k], = x[S[k]] + epos[k] - eneg[k];

s.t. C3 {k in SENSORS} :
	epos[k], <= Emax[k] + BigM * gerr[k];

s.t. C4 {k in SENSORS} :
	eneg[k], <= Emax[k] + BigM * gerr[k];

s.t. C5 {j in STREAMS} :
	x[j], >= 0;


solve;


data;

set UNITS :=;

set SENSORS :=;

set STREAMS :=;

param BigM := 0;

param A :=;

param Emax :=;

param S :=;

param Y :=;


end;
