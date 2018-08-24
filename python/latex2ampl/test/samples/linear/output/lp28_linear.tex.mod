set PROD;

param T, > 0;

param rate{p in PROD}, > 0;

set AREA{p in PROD};

param invcost{p in PROD}, >= 0;

param revenue{p in PROD, a in AREA[p], t in 1..T}, >= 0;

param Make{p in PROD, t in 1..T}, >= 0;

param inv0{p in PROD}, >= 0;

param avail{t in 1..T}, >= 0;

param prodcost{p in PROD}, >= 0;

param Inv{p in PROD, t0 in 0..T}, >= 0;

param market{p in PROD, a in AREA[p], t in 1..T}, >= 0;

param Sell{p in PROD, a in AREA[p], t in 1..T}, <= market[p,a,t], >= 0;


maximize obj: sum{p in PROD, t in 1..T}(sum{a in AREA[p]}revenue[p,a,t] * Sell[p,a,t] - prodcost[p] * Make[p,t] - invcost[p] * Inv[p,t]);

s.t. C1 {t in 1..T} :
	sum{p in PROD}(1/rate[p]) * Make[p,t] <= avail[t];

s.t. C2 {p in PROD} :
	Inv[p,0] = inv0[p];

s.t. C3 {p in PROD, t in 1..T} :
	Make[p,t] + Inv[p,t - 1] = sum{a in AREA[p]}Sell[p,a,t] + Inv[p,t];


