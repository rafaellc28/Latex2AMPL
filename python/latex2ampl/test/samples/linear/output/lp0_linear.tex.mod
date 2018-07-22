set INPUT;

set OUTPUT;

param in_min{i in INPUT}, >= 0;

param cost{i in INPUT}, > 0;

param io{o in OUTPUT, i in INPUT}, >= 0;

param out_min{o in OUTPUT}, >= 0;

param out_max{o in OUTPUT}, >= out_min[o];

param in_max{i in INPUT}, >= in_min[i];


var X{j in INPUT}, <= in_max[j], >= in_min[j];


minimize obj: sum{j in INPUT}cost[j] * X[j];

s.t. C1 {i in OUTPUT} :
	out_min[i] <= sum{j in INPUT}io[i,j] * X[j] <= out_max[i];


