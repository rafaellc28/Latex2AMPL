param NPeriods;

set PERIODS;

param Kstrike;

set STATES{p in PERIODS};

param S{p in PERIODS, s in STATES[p]};

param B{p in PERIODS, s in STATES[p]};


var C{p in PERIODS, s in STATES[p]};

var x{p in PERIODS, s in STATES[p]};

var y{p in PERIODS, s in STATES[p]};


minimize obj: C[0,0];

s.t. C1 {p in PERIODS, s in STATES[p]} :
	C[p,s], = x[p,s] * B[p,s] + y[p,s] * S[p,s];

s.t. C2 {p in PERIODS, s in STATES[p] : p < NPeriods} :
	x[p,s] * B[p + 1,s] + y[p,s] * S[p + 1,s], >= C[p + 1,s];

s.t. C3 {p in PERIODS, s in STATES[p] : p < NPeriods} :
	x[p,s] * B[p + 1,s + 1] + y[p,s] * S[p + 1,s + 1], >= C[p + 1,s + 1];

s.t. C4 {p in PERIODS, s in STATES[p] : p < NPeriods} :
	x[p,s] * B[p + 1,s] + y[p,s] * S[p + 1,s], >= S[p + 1,s] - Kstrike;

s.t. C5 {p in PERIODS, s in STATES[p] : p < NPeriods} :
	x[p,s] * B[p + 1,s + 1] + y[p,s] * S[p + 1,s + 1], >= S[p + 1,s + 1] - Kstrike;

s.t. C6 {s in STATES[NPeriods]} :
	C[NPeriods,s], >= max(0,S[NPeriods,s] - Kstrike);


solve;


data;

param NPeriods := 0;

set PERIODS :=;

param Kstrike := 0;

set STATES[0] :=;

param S :=;

param B :=;


end;
