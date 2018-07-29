set DEST;

set ORIG;

param rate{o in ORIG, d in DEST}, >= 0;

param demand{d in DEST}, >= 0;

param limit{o in ORIG, d in DEST}, > 0;

param supply{o in ORIG}, >= 0;


var Trans{i in ORIG, j in DEST}, >= 0;


minimize obj: sum{i in ORIG, j in DEST}rate[i,j] * Trans[i,j] / (1 - Trans[i,j] / limit[i,j]);

s.t. C1 {i in ORIG} :
	sum{j in DEST}Trans[i,j] = supply[i];

s.t. C2 {j in DEST} :
	sum{i in ORIG}Trans[i,j] = demand[j];


