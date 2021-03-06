set PLANTS;

set SCENARIOS;

set DEMAND;

param C{p in PLANTS};

param e{p in PLANTS};

param D{d in DEMAND, s in SCENARIOS};

param O{p in PLANTS};

param T{d in DEMAND};


var capcost;

var y{p in PLANTS, d in DEMAND, s in SCENARIOS} >= 0;

var x{p in PLANTS} >= 0;

var v{s in SCENARIOS};


minimize obj: capcost + sum{s in SCENARIOS}0.25 * v[s];

s.t. C1 : capcost = sum{p in PLANTS}C[p] * (e[p] + x[p]);

s.t. C2 {s in SCENARIOS} :
	v[s] = sum{p in PLANTS, d in DEMAND}T[d] * O[p] * y[p,d,s];

s.t. C3 {p in PLANTS, s in SCENARIOS} :
	e[p] + x[p] >= sum{d in DEMAND}y[p,d,s];

s.t. C4 {d in DEMAND, s in SCENARIOS} :
	D[d,s] = sum{p in PLANTS}y[p,d,s];


