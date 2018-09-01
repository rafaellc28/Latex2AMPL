set DEST;

set PROD;

param minload, >= 0;

set ORIG;

param vcost{o in ORIG, d in DEST, p in PROD}, >= 0;

param demand{d in DEST, p in PROD}, >= 0;

param fcost{o in ORIG, d in DEST}, >= 0;

param limit{o in ORIG, d in DEST}, >= 0;

param supply{o in ORIG, p in PROD}, >= 0;


var Use{o in ORIG, d in DEST} binary;

var Trans{o in ORIG, d in DEST, p in PROD}, >= 0;


minimize obj: sum{i in ORIG, j in DEST, p in PROD}vcost[i,j,p] * Trans[i,j,p] + sum{i in ORIG, j in DEST}fcost[i,j] * Use[i,j];

s.t. C1 {i in ORIG, p in PROD} :
	sum{j in DEST}Trans[i,j,p] = supply[i,p];

s.t. C2 {j in DEST, p in PROD} :
	sum{i in ORIG}Trans[i,j,p] = demand[j,p];

s.t. C3 {i in ORIG, j in DEST} :
	sum{p in PROD}Trans[i,j,p] <= limit[i,j] * Use[i,j];

s.t. C4 {i in ORIG, j in DEST} :
	sum{p in PROD}Trans[i,j,p] >= minload * Use[i,j];


