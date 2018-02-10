set prd;

param life integer, > 0;

param sl, > 0;

param rir, >= 0;

param iw integer, >= 0;

param rtr, > 0;

param cs integer, > 0;

param pir, >= 0;

param first integer, > 0;

param crs{p in prd}, > 0;

param last integer, > first;

param pt{p in prd}, > 0;

param pc{p in prd}, > 0;

param iinv{p in prd}, >= 0;

param cri{p in prd}, > 0;

param otr, > rtr;

param pro{p in prd, i in first..last + 1} logical;

param dem{p in prd, i in first..last + 1}, >= 0;

set time2, := first..last;

param ol{t in time2}, >= 0;

param cmin{t in time2}, >= 0;

param dpp{t in time2}, > 0;

param hc{t in time2}, >= 0;

param iil{p in prd, t in time2}, := iinv[p] less sum{v in first..t}dem[p,v];

param minv{p in prd, t in time2}, := dem[p,t + 1] * (if pro[p,t + 1] then pir else rir);

param lc{t in time2}, >= 0;

param cmax{t in time2}, >= cmin[t];


var Rprd{p in prd, t in time2} >= 0;

var Hire{t in time2} >= 0;

var Layoff{t in time2} >= 0;

var Inv{p in prd, t in time2, a in 1..life} >= 0;

var Oprd{p in prd, t in time2} >= 0;

var Short{p in prd, t in time2} >= 0;

var Crews{t in first - 1..last} >= 0;


minimize obj: sum{t in time2}rtr * sl * dpp[t] * cs * Crews[t] + sum{t in time2}hc[t] * Hire[t] + sum{t in time2}lc[t] * Layoff[t] + sum{t in time2, p in prd}otr * cs * pt[p] * Oprd[p,t] + sum{t in time2, p in prd, a in 1..life}cri[p] * pc[p] * Inv[p,t,a] + sum{t in time2, p in prd}crs[p] * pc[p] * Short[p,t];

s.t. C1 {t in time2} :
	sum{p in prd}pt[p] * Rprd[p,t] <= sl * dpp[t] * Crews[t];

s.t. C2 {t in time2} :
	sum{p in prd}pt[p] * Oprd[p,t] <= ol[t];

s.t. C3 : Crews[first - 1] = iw;

s.t. C4 {t in time2} :
	Crews[t] = Crews[t - 1] + Hire[t] - Layoff[t];

s.t. C5 {t in time2} :
	cmin[t] <= Crews[t] <= cmax[t];

s.t. C6 {p in prd} :
	Rprd[p,first] + Oprd[p,first] + Short[p,first] - Inv[p,first,1] = dem[p,first] less iinv[p];

s.t. C7 {p in prd, t in first + 1..last} :
	Rprd[p,t] + Oprd[p,t] + Short[p,t] - Short[p,t - 1] + sum{a in 1..life}(Inv[p,t - 1,a] - Inv[p,t,a]) = dem[p,t] less iil[p,t - 1];

s.t. C8 {p in prd, t in time2} :
	sum{a in 1..life}Inv[p,t,a] + iil[p,t] >= minv[p,t];

s.t. C9 {p in prd, v in 1..life - 1, a in v + 1..life} :
	Inv[p,first + v - 1,a] = 0;

s.t. C10 {p in prd, t in time2} :
	Inv[p,t,1] <= Rprd[p,t] + Oprd[p,t];

s.t. C11 {p in prd, t in first + 1..last, a in 2..life} :
	Inv[p,t,a] <= Inv[p,t - 1,a - 1];


