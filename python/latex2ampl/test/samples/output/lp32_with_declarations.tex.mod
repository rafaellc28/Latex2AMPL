param Rf, := 0.03;

set EXPENSES, := {"TuitionA","TuitionB","TuitionC"};

param T, := 40;

param Wi, := 0;

param Ri, := 0.05;

param Nper, := 1 * T;

param dT, := T / Nper;

set N, := 0..Nper;

param rf, := Rf * dT;

param t{n in N}, := n * dT;

param ri, := Ri * dT;

param salary{n in N}, := (150000 * (1 + rf) ^ n) * (0.4 + 0.1 * t[n]) / (1 + 0.1 * t[n]);


var fSave;

var x{n in N, e in EXPENSES} >= 0;

var u{n in N} >= 0;

var w{n in N} >= 0;


minimize obj: fSave;

s.t. C1  : w[Nper] = 8 * salary[Nper];

s.t. C2 {n in 18 / dT..21 / dT} :
	x[n,"TuitionA"] = 40000 * (1 + Rf) ^ n;

s.t. C3 {n in 20 / dT..23 / dT} :
	x[n,"TuitionB"] = 40000 * (1 + Rf) ^ n;

s.t. C4 {n in 22 / dT..25 / dT} :
	x[n,"TuitionC"] = 40000 * (1 + Rf) ^ n;

s.t. C5  : w[0] = Wi;

s.t. C6 {n in 1..Nper} :
	w[n] = (1 + Ri) * (w[n - 1] + u[n - 1]) - sum{e in EXPENSES}x[n,e];

s.t. C7 {n in 0..Nper} :
	u[n] <= fSave * salary[n];


