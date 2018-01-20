param section integer, > 0;

set cities;

param last integer, > 0;

set links dimen 2, within {c1 in cities, c2 in cities : c1 != c2};

set times, := 1..last;

param disttable{(l1,l2) in links}, >= 0, default 0.0;

set schedule dimen 4, within {c1 in cities, t1 in times, c2 in cities, t2 in times : (c1,c2) in links};

param distance{(c1,c2) in links}, > 0, := if disttable[c1,c2] > 0 then disttable[c1,c2] else disttable[c2,c1];

param demand{(c1,t1,c2,t2) in schedule}, > 0;

param high{(c1,t1,c2,t2) in schedule}, := max(2,min(ceil(2 * demand[c1,t1,c2,t2]),section * ceil(demand[c1,t1,c2,t2] / section)));

param low{(c1,t1,c2,t2) in schedule}, := ceil(demand[c1,t1,c2,t2]);


var X{(c1,t1,c2,t2) in schedule} >= 0;

var U{c in cities, t in times} >= 0;


minimize obj: sum{c in cities}U[c,last] + sum{(c1,t1,c2,t2) in schedule : t2 < t1}X[c1,t1,c2,t2];

minimize obj2: sum{(c1,t1,c2,t2) in schedule}distance[c1,c2] * X[c1,t1,c2,t2];

s.t. C1 {c in cities, t in times} :
	U[c,t] = U[c,if t > 1 then t - 1 else last] + sum{(c1,t1,c,t) in schedule}X[c1,t1,c,t] - sum{(c,t,c2,t2) in schedule}X[c,t,c2,t2];

s.t. C2 {(c1,t1,c2,t2) in schedule} :
	low[c1,t1,c2,t2] <= X[c1,t1,c2,t2] <= high[c1,t1,c2,t2];


