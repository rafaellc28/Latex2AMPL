set PLANTS;

set SCENARIOS;

set DEMAND;

param C{p in PLANTS};

param E{p in PLANTS};

param D{d in DEMAND, s in SCENARIOS};

param O{p in PLANTS};

param T{d in DEMAND};


var capcost;

var v{s in SCENARIOS};

var x{p in PLANTS} >= 0;

var y{p in PLANTS, d in DEMAND, s in SCENARIOS} >= 0;


minimize obj: capcost + sum{s in SCENARIOS}0.25 * v[s];

s.t. C1  : capcost, = sum{p in PLANTS}C[p] * (E[p] + x[p]);

s.t. C2 {s in SCENARIOS} :
	v[s], = sum{p in PLANTS, d in DEMAND}T[d] * O[p] * y[p,d,s];

s.t. C3 {p in PLANTS, s in SCENARIOS} :
	E[p] + x[p], >= sum{d in DEMAND}y[p,d,s];

s.t. C4 {d in DEMAND, s in SCENARIOS} :
	D[d,s], = sum{p in PLANTS}y[p,d,s];


solve;


data;

set PLANTS :=;

set SCENARIOS :=;

set DEMAND :=;

param C :=;

param E :=;

param D :=;

param O :=;

param T :=;


end;
