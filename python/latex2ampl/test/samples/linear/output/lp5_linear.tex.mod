set PROD;

set ACT;

param level_max{a in ACT}, > 0;

param cost{a in ACT}, > 0;

param io{p in PROD, a in ACT}, >= 0;

param level_min{a in ACT}, > 0;

param demand{p in PROD}, >= 0;

param Level{j in ACT}, <= level_max[j], >= level_min[j];


minimize obj: sum{j in ACT}cost[j] * Level[j];

s.t. C1 {i in PROD} :
	sum{j in ACT}io[i,j] * Level[j] >= demand[i];


