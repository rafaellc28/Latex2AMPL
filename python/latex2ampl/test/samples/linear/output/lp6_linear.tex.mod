set PROD;

set ACT;

param cost{a in ACT}, > 0;

param io{p in PROD, a in ACT}, >= 0;

param demand{p in PROD}, >= 0;


var Level{j in ACT}, >= 0;


minimize obj: sum{j in ACT}cost[j] * Level[j];

s.t. C1 {i in PROD} :
	sum{j in ACT}io[i,j] * Level[j] >= demand[i];


