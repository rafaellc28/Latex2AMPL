set WEEKS ordered;

set PROD;

param invcost{p in PROD}, >= 0;

param revenue{p in PROD, w in WEEKS}, >= 0;

param Make{p in PROD, w in WEEKS}, >= 0;

param inv0{p in PROD}, >= 0;

param avail{w in WEEKS}, >= 0;

param rate{p in PROD}, > 0;

param prodcost{p in PROD}, >= 0;

param Inv{p in PROD, w in WEEKS}, >= 0;

param market{p in PROD, w in WEEKS}, >= 0;

param Sell{p in PROD, w in WEEKS}, <= market[p,w], >= 0;


maximize obj: sum{p in PROD, t in WEEKS}(revenue[p,t] * Sell[p,t] - prodcost[p] * Make[p,t] - invcost[p] * Inv[p,t]);

s.t. C1 {t in WEEKS} :
	sum{p in PROD}(1/rate[p]) * Make[p,t] <= avail[t];

s.t. C2 {p in PROD} :
	Make[p,first(WEEKS)] + inv0[p] = Sell[p,first(WEEKS)] + Inv[p,first(WEEKS)];

s.t. C3 {p in PROD, t in WEEKS : ord(t) > 1} :
	Make[p,t] + Inv[p,prev(t)] = Sell[p,t] + Inv[p,t];


