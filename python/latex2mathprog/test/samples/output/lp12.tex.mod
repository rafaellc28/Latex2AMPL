param K;

set J;

set M;

param MS integer;

param P{j in J, a in M};

param Sigma{j in J, t in 1..MS};


var x{j in J, a in M} >= 0;

var Y{i in J, j in J, a in M} binary;

var z;


minimize obj: z;

s.t. C1 {j in J, t in 2..MS} :
	x[j,Sigma[j,t]], >= x[j,Sigma[j,t - 1]] + P[j,Sigma[j,t - 1]];

s.t. C2 {i in J, j in J, a in M : i <> j} :
	x[i,a], >= x[j,a] + P[j,a] - K * Y[i,j,a];

s.t. C3 {i in J, j in J, a in M : i <> j} :
	x[j,a], >= x[i,a] + P[i,a] - K * (1 - Y[i,j,a]);

s.t. C4 {j in J} :
	z, >= x[j,Sigma[j,MS]] + P[j,Sigma[j,MS]];

s.t. C5 {j in J, t in 1..MS} :
	MS, >= Sigma[j,t], >= 1;

s.t. C6 {j in J, a in M} :
	P[j,a], >= 0;

s.t. C7 {j in J, a in M} :
	x[j,a], >= 0;


solve;


data;

param K := 0;

set J :=;

set M :=;

param MS := 0;

param P :=;

param Sigma :=;


end;
