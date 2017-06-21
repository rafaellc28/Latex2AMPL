set cities;

set times;

param Last integer;

set Links dimen 2;

set schedule dimen 4;

param High{(c1,t1,c2,t2) in schedule};

param Distance{(c1,c2) in Links};

param Low{(c1,t1,c2,t2) in schedule};


var X{(c1,t1,c2,t2) in schedule} >= 0;

var U{c in cities, t in times} >= 0;


minimize obj1: sum{c in cities}U[c,Last] + sum{(c1,t1,c2,t2) in schedule : t2 < t1}X[c1,t1,c2,t2];

minimize obj2: sum{(c1,t1,c2,t2) in schedule}Distance[c1,c2] * X[c1,t1,c2,t2];

s.t. C1 {c in cities, t in times} :
	U[c,t], = U[c,if t > 1 then t - 1 else Last] + sum{(c1,t1,c,t) in schedule}X[c1,t1,c,t] - sum{(c,t,c2,t2) in schedule}X[c,t,c2,t2];

s.t. C2 {(c1,t1,c2,t2) in schedule} :
	Low[c1,t1,c2,t2], <= X[c1,t1,c2,t2], <= High[c1,t1,c2,t2];

s.t. C3 {(c1,c2) in Links} :
	Distance[c1,c2], >= 0;


solve;


data;

set cities :=;

set times :=;

param Last := 0;

set Links :=;

set schedule :=;

param High :=;

param Distance :=;

param Low :=;


end;
