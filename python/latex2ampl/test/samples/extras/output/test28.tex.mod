set DEST;

set PROD;

param maxserve;

set ORIG;


var Trans{i in ORIG, j in DEST, p in PROD} >= 0;


s.t. C1 {i in ORIG} :
	count {j in DEST} (sum{p in PROD}Trans[i,j,p] > 0) <= maxserve;


