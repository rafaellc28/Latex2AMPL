set FEEDS;

set CITIES;

set PRODS;

set LINKS dimen 2, within (CITIES cross CITIES);

param capacity{p in PRODS, (i,j) in LINKS}, >= 0;

param supply{p in PRODS, c in CITIES}, >= 0;

param yield{p in PRODS, f in FEEDS}, >= 0;

param cost{p in PRODS, (i,j) in LINKS}, >= 0;

param limit{f in FEEDS, p in PRODS}, >= 0;

param demand{p in PRODS, c in CITIES}, >= 0;


var Feed{f in FEEDS, k in CITIES} >= 0, <= limit[f,k];


minimize Total_Cost;

node Balance {p in PRODS, k in CITIES} :
	net_out = supply[p,k] - demand[p,k] + sum{f in FEEDS}yield[p,f] * Feed[f,k];

arc Ship {p in PRODS, (i,j) in LINKS} >= 0, <= capacity[p,i,j],
	 from Balance[p,i], to Balance[p,j], obj Total_Cost cost[p,i,j];


