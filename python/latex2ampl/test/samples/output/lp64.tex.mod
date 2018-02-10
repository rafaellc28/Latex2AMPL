set prd;

param Life integer;

param Last integer;

param Rtr;

set time2;

param Iw integer;

param Sl;

param Cs integer;

param Otr;

param First integer;

param Crs{p in prd};

param Ol{t in time2};

param Lc{t in time2};

param Pt{p in prd};

param Dpp{t in time2};

param Pc{p in prd};

param Dem{p in prd, t in First..Last + 1};

param Hc{t in time2};

param Iil{p in prd, t in time2};

param Iinv{p in prd};

param Cmax{t in time2};

param Cri{p in prd};

param Minv{p in prd, t in time2};

param Cmin{t in time2};


var Rprd{p in prd, t in time2} >= 0;

var Hire{t in time2} >= 0;

var Layoff{t in time2} >= 0;

var Inv{p in prd, t in time2, a in 1..Life} >= 0;

var Oprd{p in prd, t in time2} >= 0;

var Short{p in prd, t in time2} >= 0;

var Crews{t in First - 1..Last} >= 0;


minimize obj: sum{t in time2}Rtr * Sl * Dpp[t] * Cs * Crews[t] + sum{t in time2}Hc[t] * Hire[t] + sum{t in time2}Lc[t] * Layoff[t] + sum{t in time2, p in prd}Otr * Cs * Pt[p] * Oprd[p,t] + sum{t in time2, p in prd, a in 1..Life}Cri[p] * Pc[p] * Inv[p,t,a] + sum{t in time2, p in prd}Crs[p] * Pc[p] * Short[p,t];

s.t. C1 {t in time2} :
	sum{p in prd}Pt[p] * Rprd[p,t] <= Sl * Dpp[t] * Crews[t];

s.t. C2 {t in time2} :
	sum{p in prd}Pt[p] * Oprd[p,t] <= Ol[t];

s.t. C3 : Crews[First - 1] = Iw;

s.t. C4 {t in time2} :
	Crews[t] = Crews[t - 1] + Hire[t] - Layoff[t];

s.t. C5 {t in time2} :
	Cmin[t] <= Crews[t] <= Cmax[t];

s.t. C6 {p in prd} :
	Rprd[p,First] + Oprd[p,First] + Short[p,First] - Inv[p,First,1] = Dem[p,First] less Iinv[p];

s.t. C7 {p in prd, t in First + 1..Last} :
	Rprd[p,t] + Oprd[p,t] + Short[p,t] - Short[p,t - 1] + sum{a in 1..Life}(Inv[p,t - 1,a] - Inv[p,t,a]) = Dem[p,t] less Iil[p,t - 1];

s.t. C8 {p in prd, t in time2} :
	sum{a in 1..Life}Inv[p,t,a] + Iil[p,t] >= Minv[p,t];

s.t. C9 {p in prd, v in 1..Life - 1, a in v + 1..Life} :
	Inv[p,First + v - 1,a] = 0;

s.t. C10 {p in prd, t in time2} :
	Inv[p,t,1] <= Rprd[p,t] + Oprd[p,t];

s.t. C11 {p in prd, t in First + 1..Last, a in 2..Life} :
	Inv[p,t,a] <= Inv[p,t - 1,a - 1];

s.t. C12 {p in prd, t in time2, a in 1..Life} :
	Inv[p,t,a] >= 0;

s.t. C13 {p in prd, t in time2} :
	Short[p,t] >= 0;

s.t. C14 {t in First - 1..Last} :
	Crews[t] >= 0;

s.t. C15 {p in prd, t in First..Last + 1} :
	Dem[p,t] >= 0;


