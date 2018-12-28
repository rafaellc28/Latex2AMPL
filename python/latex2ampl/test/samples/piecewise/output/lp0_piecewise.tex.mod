set DEST;

set ORIG;

param demand{j in DEST}, >= 0;

param limit1{i in ORIG, j in DEST}, > 0;

param rate1{i in ORIG, j in DEST}, >= 0;

param supply{i in ORIG}, >= 0;

param rate2{i in ORIG, j in DEST}, >= rate1[i,j];

param limit2{i in ORIG, j in DEST}, > limit1[i,j];

param rate3{i in ORIG, j in DEST}, >= rate2[i,j];


var Trans{i in ORIG, j in DEST} >= 0;


minimize obj: sum{i in ORIG, j in DEST} << limit1[i,j], limit2[i,j]; rate1[i,j], rate2[i,j], rate3[i,j] >> Trans[i,j];

s.t. C1 {i in ORIG} :
	sum{j in DEST}Trans[i,j] = supply[i];

s.t. C2 {j in DEST} :
	sum{i in ORIG}Trans[i,j] = demand[j];


