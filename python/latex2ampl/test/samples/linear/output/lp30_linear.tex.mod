param life integer, > 0;

param sl, > 0;

param rir, >= 0;

param iw integer, >= 0;

param rtr, > 0;

param cs integer, > 0;

param pir, >= 0;

set prod;

param first integer, > 0;

param otr, > rtr;

param last integer, > first;

set time2, := first..last;

param crs{p in prod}, > 0;

param ol{t in time2}, >= 0;

param lc{t in time2}, >= 0;

param pt{p in prod}, > 0;

param dpp{t in time2}, > 0;

param pro{p in prod, i in first..last + 1} logical;

param pc{p in prod}, > 0;

param dem{p in prod, i in first..last + 1}, >= 0;

param hc{t in time2}, >= 0;

param iinv{p in prod}, >= 0;

param cri{p in prod}, > 0;

param cmin{t in time2}, >= 0;

param iil{p in prod, t in time2}, := if iinv[p] < sum{v in first..t}dem[p,v] then 0 else iinv[p] - sum{v in first..t}dem[p,v];

param cmax{t in time2}, >= cmin[t];

param minv{p in prod, t in time2}, := dem[p,t + 1] * (if pro[p,t + 1] then pir else rir);


var Oprod{p in prod, t in time2}, >= 0;

var Hire{t in time2}, >= 0;

var Layoff{t in time2}, >= 0;

var Inv{p in prod, t in time2, j in 1..life}, >= 0;

var Rprod{p in prod, t in time2}, >= 0;

var Short{p in prod, t in time2}, >= 0;

var Crews{i in first - 1..last}, >= 0;


minimize obj: sum{t in time2}rtr * sl * dpp[t] * cs * Crews[t] + sum{t in time2}hc[t] * Hire[t] + sum{t in time2}lc[t] * Layoff[t] + sum{t in time2, p in prod}otr * cs * pt[p] * Oprod[p,t] + sum{t in time2, p in prod, a in 1..life}cri[p] * pc[p] * Inv[p,t,a] + sum{t in time2, p in prod}crs[p] * pc[p] * Short[p,t];

s.t. C1 {t in time2} :
	sum{p in prod}pt[p] * Rprod[p,t] != 0 <== sl * dpp[t] * Crews[t] != 0;

s.t. C2 {t in time2} :
	sum{p in prod}pt[p] * Oprod[p,t] <= ol[t];

s.t. C3 : Crews[first - 1] = iw;

s.t. C4 {t in time2} :
	Crews[t] = Crews[t - 1] + Hire[t] - Layoff[t];

s.t. C5 {t in time2} :
	cmin[t] <= Crews[t] <= cmax[t];

s.t. C6 {p in prod} :
	Rprod[p,first] + Oprod[p,first] + Short[p,first] - Inv[p,first,1] = if dem[p,first] < iinv[p] then 0 else dem[p,first] - iinv[p];

s.t. C7 {p in prod, t in first + 1..last} :
	Rprod[p,t] + Oprod[p,t] + Short[p,t] - Short[p,t - 1] + sum{a in 1..life}(Inv[p,t - 1,a] - Inv[p,t,a]) = if dem[p,t] < iil[p,t - 1] then 0 else dem[p,t] - iil[p,t - 1];

s.t. C8 {p in prod, t in time2} :
	sum{a in 1..life}Inv[p,t,a] + iil[p,t] >= minv[p,t];

s.t. C9 {p in prod, v in 1..life - 1, a in v + 1..life} :
	Inv[p,first + v - 1,a] = 0;

s.t. C10 {p in prod, t in time2} :
	Inv[p,t,1] <= Rprod[p,t] + Oprod[p,t];

s.t. C11 {p in prod, t in first + 1..last, a in 2..life} :
	Inv[p,t,a] <= Inv[p,t - 1,a - 1];


