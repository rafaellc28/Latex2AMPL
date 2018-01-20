set DEST;

set PROD;

param minload;

set ORIG;

param limit{i in ORIG, j in DEST};


var Use{i in ORIG, j in DEST} binary;

var Trans{i in ORIG, j in DEST, p in PROD} >= 0;


s.t. C1 {i in ORIG, j in DEST} :
	sum{p in PROD}Trans[i,j,p] <= limit[i,j] * Use[i,j];

s.t. C2 {i in ORIG, j in DEST} :
	sum{p in PROD}Trans[i,j,p] >= minload * Use[i,j];


