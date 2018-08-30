set DEST;

set PROD;

set ORIG;

param demand{d in DEST, p in PROD}, >= 0;

param cost{o in ORIG, d in DEST, p in PROD}, >= 0;

param limit{o in ORIG, d in DEST}, >= 0;

param supply{o in ORIG, p in PROD}, >= 0;


var Trans{o in ORIG, d in DEST, p in PROD}, >= 0;


minimize obj: sum{i in ORIG, j in DEST, p in PROD}cost[i,j,p] * Trans[i,j,p];

s.t. C1 {i in ORIG, p in PROD} :
	sum{j in DEST}Trans[i,j,p] = supply[i,p];

s.t. C2 {j in DEST, p in PROD} :
	sum{i in ORIG}Trans[i,j,p] = demand[j,p];

s.t. C3 {i in ORIG, j in DEST} :
	sum{p in PROD}Trans[i,j,p] <= limit[i,j];


