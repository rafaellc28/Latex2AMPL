set CITIES;

set PRODS;

set LINKS dimen 2, within (CITIES cross CITIES);

param capacity{(i,j) in LINKS, p in PRODS}, >= 0;

param supply{c in CITIES, p in PRODS}, >= 0;

param cost{(i,j) in LINKS, p in PRODS}, >= 0;

param demand{c in CITIES, p in PRODS}, >= 0;

param cap_joint{(i,j) in LINKS}, >= 0;


minimize Total_Cost;

node Balance {k in CITIES, p in PRODS} :
	net_in = demand[k,p] - supply[k,p];

s.t. Multi {(i,j) in LINKS} :
	to_come <= cap_joint[i,j];

arc Ship {(i,j) in LINKS, p in PRODS} >= 0, <= capacity[i,j,p],
	 from Balance[i,p], to Balance[j,p], coeff Multi[i,j] 1.0, obj Total_Cost cost[i,j,p];


