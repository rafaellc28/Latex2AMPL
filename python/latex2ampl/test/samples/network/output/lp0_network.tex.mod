set CITIES;

set LINKS dimen 2, within (CITIES cross CITIES);

param demand{c in CITIES}, >= 0;

param cost{(i,j) in LINKS}, >= 0;

param capacity{(i,j) in LINKS}, >= 0;

param supply{c in CITIES}, >= 0;


minimize Total_Cost;

node Balance {k in CITIES} :
	net_in = demand[k] - supply[k];

arc Ship {(i,j) in LINKS} >= 0, <= capacity[i,j],
	 from Balance[i], to Balance[j], obj Total_Cost cost[i,j];


