set CITIES;

set PRODS;

set LINKS dimen 2, within (CITIES cross CITIES);

param cap_joint{(i,j) in LINKS}, >= 0;

param supply{c in CITIES, p in PRODS}, >= 0;

param cost{(i,j) in LINKS, p in PRODS}, >= 0;

param demand{c in CITIES, p in PRODS}, >= 0;

param capacity{(i,j) in LINKS, p in PRODS}, >= 0;


minimize Total_Cost;

node Balance {k in CITIES, p in PRODS} :
	net_in = demand[k,p] - supply[k,p];

arc Ship {(i,j) in LINKS, p in PRODS} >= 0, <= capacity[i,j,p],
	 from Balance[i,p], to Balance[j,p], obj Total_Cost cost[i,j,p];

s.t. C1 {(i,j) in LINKS} :
	sum{p in PRODS}Ship[i,j,p] <= cap_joint[i,j];


