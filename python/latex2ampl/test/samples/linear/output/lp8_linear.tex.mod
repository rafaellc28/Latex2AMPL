set PROJECTS;

set PEOPLE;

param demand{p in PROJECTS}, >= 0;

param cost{i in PEOPLE, j in PROJECTS}, >= 0;

param limit{i in PEOPLE, j in PROJECTS}, >= 0;

param supply{p in PEOPLE}, >= 0;


var M;

var Assign{i in PEOPLE, j in PROJECTS}, <= limit[i,j], >= 0;


minimize obj: M;

s.t. C1 {i in PEOPLE} :
	M >= sum{j in PROJECTS}cost[i,j] * Assign[i,j];

s.t. C2 {i in PEOPLE} :
	sum{j in PROJECTS}Assign[i,j] = supply[i];

s.t. C3 {j in PROJECTS} :
	sum{i in PEOPLE}Assign[i,j] = demand[j];


