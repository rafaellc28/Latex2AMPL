set PROD;

set ACT;

param io{i in PROD, j in ACT};

param Level{j in ACT};

param level_max{j in ACT};

param Price{i in PROD};

param cost{j in ACT};

param level_min{j in ACT};


s.t. C1 {j in ACT} :
	level_min[j] <= Level[j] <= level_max[j] complements cost[j] - sum{i in PROD}Price[i] * io[i,j];


