set FOOD;

set NUTR;

param cost{f in FOOD}, > 0;

param n_min{n in NUTR}, >= 0;

param f_min{f in FOOD}, >= 0;

param amt{n in NUTR, f in FOOD}, >= 0;

param f_max{f in FOOD}, >= f_min[f];

param n_max{n in NUTR}, >= n_min[n];


var Buy{f in FOOD}, <= f_max[f], >= f_min[f];


minimize obj: sum{j in FOOD}cost[j] * Buy[j];

s.t. C1 {i in NUTR} :
	n_min[i] <= sum{j in FOOD}amt[i,j] * Buy[j] <= n_max[i];


