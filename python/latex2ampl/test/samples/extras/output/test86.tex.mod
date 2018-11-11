set CITIES;

set LINKS dimen 2;

param capacity{(i,j) in LINKS};

param supply{k in CITIES};

param cost{(i,j) in LINKS};

param demand{k in CITIES};


minimize Total_Cost;

node Balance {k in CITIES} :
	net_in = demand[k] - supply[k];

arc Ship {(i,j) in LINKS} >= 0, <= capacity[i,j],
	 from Balance[i], to Balance[j], obj Total_Cost cost[i,j];


