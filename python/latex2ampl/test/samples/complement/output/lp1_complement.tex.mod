set PROD;

set ACT;

param level_max{j in ACT}, > 0;

param cost{j in ACT}, > 0;

param level_min{j in ACT}, > 0;

param io{i in PROD, j in ACT}, >= 0;

param demand{i in PROD}, >= 0;


var Price{i in PROD};

var Level{j in ACT};


s.t. C1 {i in PROD} :
	Price[i] >= 0 complements sum{j in ACT}io[i,j] * Level[j] >= demand[i];

s.t. C2 {j in ACT} :
	level_min[j] <= Level[j] <= level_max[j] complements cost[j] - sum{i in PROD}Price[i] * io[i,j];


