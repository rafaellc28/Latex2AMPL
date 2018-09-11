set DEST;

set LINKS dimen 2;

set ORIG;

param demand{d in DEST};

param cost{(i,j) in LINKS}, >= 0;

param supply{o in ORIG};


var Trans{(i,j) in LINKS}, >= 0;


minimize obj: sum{(i,j) in LINKS}cost[i,j] * Trans[i,j];

s.t. C1 {i in ORIG} :
	sum{(i,j) in LINKS}Trans[i,j] = supply[i];

s.t. C2 {j in DEST} :
	sum{(i,j) in LINKS}Trans[i,j] = demand[j];


