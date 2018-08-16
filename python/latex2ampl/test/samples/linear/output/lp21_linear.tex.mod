set DEST;

set PROD;

set ORIG;

param avail{o in ORIG};

param trans_cost{o in ORIG, d in DEST, p in PROD};

param rate{o in ORIG, p in PROD}, > 0;

param make_cost{o in ORIG, p in PROD};

param demand{d in DEST, p in PROD};


var Make{o in ORIG, p in PROD}, >= 0;

var Trans{o in ORIG, d in DEST, p in PROD}, >= 0;


minimize obj: sum{i in ORIG, p in PROD}make_cost[i,p] * Make[i,p] + sum{i in ORIG, j in DEST, p in PROD}trans_cost[i,j,p] * Trans[i,j,p];

s.t. C1 {i in ORIG} :
	sum{p in PROD}(1/rate[i,p]) * Make[i,p] <= avail[i];

s.t. C2 {i in ORIG, p in PROD} :
	sum{j in DEST}Trans[i,j,p] = Make[i,p];

s.t. C3 {j in DEST, p in PROD} :
	sum{i in ORIG}Trans[i,j,p] = demand[j,p];


