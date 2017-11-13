param Wi;

set EXPENSES;

param Rf;

param Nper;

param DT;

set N;

param Ri;

param Salary{n in N};


var fSave;

var x{n in 1..Nper, e in EXPENSES} >= 0;

var u{n in N} >= 0;

var w{n in N} >= 0;


minimize obj: fSave;

s.t. C1  : w[Nper] = 8 * Salary[Nper];

s.t. C2 {n in 18 / DT..21 / DT} :
	x[n,"TuitionA"] = 40000 * (1 + Rf) ^ n;

s.t. C3 {n in 20 / DT..23 / DT} :
	x[n,"TuitionB"] = 40000 * (1 + Rf) ^ n;

s.t. C4 {n in 22 / DT..25 / DT} :
	x[n,"TuitionC"] = 40000 * (1 + Rf) ^ n;

s.t. C5  : w[0] = Wi;

s.t. C6 {n in 1..Nper} :
	w[n] = (1 + Ri) * (w[n - 1] + u[n - 1]) - sum{e in EXPENSES}x[n,e];

s.t. C7 {n in 0..Nper} :
	u[n] <= fSave * Salary[n];

s.t. C8 {n in N} :
	u[n] >= 0;

s.t. C9 {n in N} :
	w[n] >= 0;

s.t. C10 {n in N} :
	Salary[n] >= 0;


