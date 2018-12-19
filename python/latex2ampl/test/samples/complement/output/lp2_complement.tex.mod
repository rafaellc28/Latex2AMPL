set PROD;

set ACT;

param demrate{i in PROD}, >= 0;

param cost{j in ACT}, > 0;

param io{i in PROD, j in ACT}, >= 0;

param demzero{i in PROD}, > 0;


var Price{i in PROD};

var Level{j in ACT};


s.t. C1 {i in PROD} :
	Price[i] >= 0 complements sum{j in ACT}io[i,j] * Level[j] >= demzero[i] - demrate[i] * Price[i];

s.t. C2 {j in ACT} :
	Level[j] >= 0 complements sum{i in PROD}Price[i] * io[i,j] <= cost[j];


