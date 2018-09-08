param section integer, > 0;

set cities;

param last integer, > 0;

set schedule dimen 4;

set times, := 1..last;

param demand{(c1,t1,c2,t2) in schedule}, > 0;


var X{(c1,t1,c2,t2) in schedule} >= 0;

var U{c in cities, t in times} >= 0;


minimize obj: sum{c in cities}U[c,last] + sum{(c1,t1,c2,t2) in schedule : t2 < t1}X[c1,t1,c2,t2];

s.t. C1 {c in cities, t in times} :
	U[c,t] = U[c,if t > 1 then t - 1 else last] + sum{(c1,t1,c,t) in schedule}X[c1,t1,c,t] - sum{(c,t,c2,t2) in schedule}X[c,t,c2,t2];

s.t. C2 {(c1,t1,c2,t2) in schedule} :
	demand[c1,t1,c2,t2] <= X[c1,t1,c2,t2] <= section * ceil(demand[c1,t1,c2,t2]/section);


