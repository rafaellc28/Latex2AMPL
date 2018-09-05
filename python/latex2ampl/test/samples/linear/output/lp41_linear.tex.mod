set PROJECTS;

set PEOPLE;

set ABILITIES dimen 2, within (PEOPLE cross PROJECTS);

param demand{pr in PROJECTS}, >= 0;

param cost{(i,j) in ABILITIES}, >= 0;

param limit{(i,j) in ABILITIES}, >= 0;

param supply{p in PEOPLE}, >= 0;


var Assign{(i,j) in ABILITIES}, <= limit[i,j], >= 0;


minimize obj: sum{(i,j) in ABILITIES}cost[i,j] * Assign[i,j];

s.t. C1 {i in PEOPLE} :
	sum{(i,j) in ABILITIES}Assign[i,j] = supply[i];

s.t. C2 {j in PROJECTS} :
	sum{(i,j) in ABILITIES}Assign[i,j] = demand[j];


