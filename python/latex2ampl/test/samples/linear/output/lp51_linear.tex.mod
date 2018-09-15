set FOOD;

set MINREQ;

set MAXREQ;

set STORE;

param lambda, := 0.85;

param f_max{j in FOOD};

param cost{s in STORE, f in FOOD}, > 0;

set NUTR, := MINREQ union MAXREQ;

param n_max{ma in MAXREQ}, >= 0;

param n_min{mi in MINREQ}, >= 0;

param f_min{f in FOOD}, >= 0;

param amt{n in NUTR, f in FOOD}, >= 0;


var Buy{j in FOOD}, <= f_max[j], >= f_min[j];


minimize obj: lambda * (sum{j in FOOD}Buy[j]) + (1 - lambda) * (sum{s in STORE}sum{j in FOOD}cost[s,j] * Buy[j]);

s.t. C1 {i in MINREQ} :
	sum{j in FOOD}amt[i,j] * Buy[j] >= n_min[i];

s.t. C2 {i in MAXREQ} :
	sum{j in FOOD}amt[i,j] * Buy[j] <= n_max[i];


