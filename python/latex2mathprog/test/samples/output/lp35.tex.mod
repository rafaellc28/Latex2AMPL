param NPeriods;

set PERIODS;

param Kstrike;

set STATES{p in PERIODS};

param S{p in PERIODS, s in STATES[p]};

param B{p in PERIODS, s in STATES[p]};


var P{p in PERIODS, s in STATES[p]};

var x{p in PERIODS, s in STATES[p]};

var y{p in PERIODS, s in STATES[p]};


minimize obj: P[0,0];

s.t. C1 {p in PERIODS, s in STATES[p]} :
	P[p,s], = x[p,s] * B[p,s] + y[p,s] * S[p,s];

s.t. C2 {p in PERIODS, s in STATES[p] : p < NPeriods} :
	x[p,s] * B[p + 1,s] + y[p,s] * S[p + 1,s], >= P[p + 1,s];

s.t. C3 {p in PERIODS, s in STATES[p] : p < NPeriods} :
	x[p,s] * B[p + 1,s + 1] + y[p,s] * S[p + 1,s + 1], >= P[p + 1,s + 1];

s.t. C4 {p in PERIODS, s in STATES[p] : p < NPeriods} :
	x[p,s] * B[p + 1,s] + y[p,s] * S[p + 1,s], >= Kstrike - S[p + 1,s];

s.t. C5 {p in PERIODS, s in STATES[p] : p < NPeriods} :
	x[p,s] * B[p + 1,s + 1] + y[p,s] * S[p + 1,s + 1], >= Kstrike - S[p + 1,s + 1];

s.t. C6 {s in STATES[NPeriods]} :
	P[NPeriods,s], >= max(0,Kstrike - S[NPeriods,s]);


solve;


data;

param NPeriods := 0;

set PERIODS :=;

param Kstrike := 0;

set STATES[0] :=;

param S :=;

param B :=;


end;
