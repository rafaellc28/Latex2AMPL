set I, := 1..16;

set K, := 1..17;

set J, := 1..18;

param xlb, >= 0, default 0;

set PAIRS dimen 2, in {J,K};

param b{i in I}, >= 0, default 0;

param c{(j,k) in PAIRS};

param E{(j,k) in PAIRS, i in I};


var x{(j,k) in PAIRS}, >= xlb, default 0.1;


minimize obj: sum{(j,k) in PAIRS}x[j,k] * (c[j,k] + log(x[j,k] / sum{m in J : (m,k) in PAIRS}x[m,k]));

s.t. C1 {i in I} :
	sum{(j,k) in PAIRS}E[j,k,i] * x[j,k] - b[i] = 0;


