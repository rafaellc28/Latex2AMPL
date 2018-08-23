set PROD;

param T, > 0;

param profit{p in PROD, t in 1..T};

param avail{t in 1..T}, >= 0;

param rate{p in PROD}, > 0;

param market{p in PROD, t in 1..T}, >= 0;


var Make{p in PROD, t in 1..T}, <= market[p,t], >= 0;


maximize obj: sum{p in PROD, t in 1..T}profit[p,t] * Make[p,t];

s.t. C1 {t in 1..T} :
	sum{p in PROD}(1/rate[p]) * Make[p,t] <= avail[t];


