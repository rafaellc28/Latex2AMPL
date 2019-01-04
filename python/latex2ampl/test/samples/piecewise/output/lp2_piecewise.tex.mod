set PROD;

param T, > 0;

param invcost{p in PROD}, >= 0;

param revenue{p in PROD, t in 1..T}, >= 0;

param avail_min{t in 1..T}, >= 0;

param inv0{p in PROD};

param rate{p in PROD}, > 0;

param time_penalty{t in 1..T}, > 0;

param prodcost{p in PROD}, >= 0;

param commit{p in PROD, t in 1..T}, >= 0;

param market{p in PROD, t in 1..T}, >= 0;

param avail_max{t in 1..T}, >= avail_min[t];

param Use{t in 1..T}, <= avail_max[t], >= 0;


var User;

var Sell{p in PROD, t in 1..T}, <= market[p,t], >= commit[p,t];

var Make{p in PROD, t in 1..T}, >= 0;

var Inv{p in PROD, t0 in 0..T}, >= 0;


maximize obj: sum{p in PROD, t in 1..T}(revenue[p,t] * Sell[p,t] - prodcost[p] * Make[p,t] - invcost[p] * Inv[p,t]) - sum{t in 1..T} << avail_min[t]; 0, time_penalty[t] >> Use[t];

s.t. C1 {t in 1..T} :
	sum{p in PROD}1/rate[p] * Make[p,t] = Use[t];

s.t. C2 {p in PROD} :
	Inv[p,0] = inv0[p];

s.t. C3 {p in PROD, t in 1..T} :
	Make[p,t] + Inv[p,t - 1] = Sell[p,t] + Inv[p,t];


