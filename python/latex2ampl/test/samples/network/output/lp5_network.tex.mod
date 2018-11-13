set CITIES;

set LINKS dimen 2, within (CITIES cross CITIES);

param supply{c in CITIES}, >= 0;

param city_cap{c in CITIES}, >= 0;

param cost{(i,j) in LINKS}, >= 0;

param demand{c in CITIES}, >= 0;

param link_cap{(i,j) in LINKS}, >= 0;


minimize Total_Cost;

node Supply {k in CITIES} :
	net_out = supply[k];

node Demand {k in CITIES} :
	net_in = demand[k];

arc Ship {(i,j) in LINKS} >= 0, <= link_cap[i,j],
	 from Demand[i], to Supply[j], obj Total_Cost cost[i,j];

arc Through {k in CITIES} >= 0, <= city_cap[k],
	 from Supply[k], to Demand[k];


