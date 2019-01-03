set DEST;

set ORIG;

param npiece{i in ORIG, j in DEST} integer, >= 1;

param rate{i in ORIG, j in DEST, p in 1..npiece[i,j]}, >= if p = 1 then 0 else rate[i,j,p - 1];

param demand{j in DEST}, >= 0;

param limit{i in ORIG, j in DEST, q in 1..npiece[i,j] - 1}, > if q = 1 then 0 else limit[i,j,q - 1];

param supply{i in ORIG}, >= 0;


var Trans{i in ORIG, j in DEST}, >= 0;


minimize obj: sum{i in ORIG, j in DEST} << {p in 1..npiece[i,j] - 1} limit[i,j,p]; {p in 1..npiece[i,j]} rate[i,j,p] >> Trans[i,j];

s.t. C1 {i in ORIG} :
	sum{j in DEST}Trans[i,j] = supply[i];

s.t. C2 {j in DEST} :
	sum{i in ORIG}Trans[i,j] = demand[j];


