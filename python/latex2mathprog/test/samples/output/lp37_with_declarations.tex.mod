param S0, := 50;

param nPeriods, := 2;

param rf, := 0.05;

param r, := 0.06;

param B0, := 1;

param Tf, := 2;

param sigma, := 0.3;

param Kstrike, := 52;

param u, := exp(sigma * sqrt(Tf / nPeriods));

set PERIODS, := {0..nPeriods};

set STATES{p in PERIODS}, := {0..p};

param d, := 1 / u;

param pr, := (exp(r * Tf / nPeriods) - d) / (u - d);

param S{p in PERIODS, s in STATES[p]}, := S0 * (d ^ (p - s)) * (u ^ s);

param B{p in PERIODS, s in STATES[p]}, := B0 * (1 + rf * Tf / nPeriods) ^ p;


var P{p in PERIODS, s in STATES[p]};

var x{p in PERIODS, s in STATES[p]};

var y{p in PERIODS, s in STATES[p]};


minimize obj: P[0,0];

s.t. C1 {p in PERIODS, s in STATES[p]} :
	P[p,s], = x[p,s] * B[p,s] + y[p,s] * S[p,s];

s.t. C2 {p in PERIODS, s in STATES[p] : p < nPeriods} :
	x[p,s] * B[p + 1,s] + y[p,s] * S[p + 1,s], >= P[p + 1,s];

s.t. C3 {p in PERIODS, s in STATES[p] : p < nPeriods} :
	x[p,s] * B[p + 1,s + 1] + y[p,s] * S[p + 1,s + 1], >= P[p + 1,s + 1];

s.t. C4 {s in STATES[nPeriods]} :
	P[nPeriods,s], >= max(0,Kstrike - S[nPeriods,s]);


solve;


end;
