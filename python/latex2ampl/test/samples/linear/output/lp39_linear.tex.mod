set CITIES;

set LINKS dimen 2, within (CITIES cross CITIES);

param demand{k in CITIES};

param cost{(i,j) in LINKS}, >= 0;

param capacity{(i,j) in LINKS}, >= 0;

param demmand{c in CITIES}, >= 0;

param supply{c in CITIES}, >= 0;

param Ship{(i,j) in LINKS}, <= capacity[i,j], >= 0;


minimize obj: sum{(i,j) in LINKS}cost[i,j] * Ship[i,j];

s.t. C1 {k in CITIES} :
	supply[k] + sum{(i,k) in LINKS}Ship[i,k] = demand[k] + sum{(k,j) in LINKS}Ship[k,j];


