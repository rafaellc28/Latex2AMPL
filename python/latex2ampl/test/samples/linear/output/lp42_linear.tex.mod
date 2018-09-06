set m_inter;

set blend dimen 2;

set m_purch;

set qual;

set m_final;

set crude;

set proc;

set unit;

set m_raw;

param attr_min{mf in m_final, q in qual}, >= 0;

param cost{p in proc}, > 0;

param io{mi in m_inter, c in crude, p in proc};

param price{cm in crude union m_purch union m_final}, > 0;

param cap{u in unit}, >= 0;

param attr_max{mf in m_final, q in qual}, >= 0;

param util{u in unit, p in proc};

param attr_crude{mi in m_inter, c in crude, q in qual}, >= 0;

param purch_max{c in crude}, > 0;

param attr_both{mf in m_final, q in qual}, >= 0;

param attr{mi in m_inter, c in crude, q in qual}, := if attr_crude[mi,c,q] > 0 then attr_crude[mi,c,q] else attr_both[mi,q];


var OperCost;

var Revenue;

var PurchCost;

var LevBl{(i,j) in blend, c in crude}, >= 0;

var InCr{c in crude}, >= 0;

var InInt{mp in m_purch, c in crude}, >= 0;

var LevPr{p in proc, c in crude}, >= 0;

var Out{mf in m_final}, >= 0;


maximize obj: Revenue - PurchCost - OperCost;

s.t. C1 {mr in m_raw, c in crude} :
	sum{p in proc}io[mr,c,p] * LevPr[p,c] + InCr[c] >= 0;

s.t. C2 {mi in m_inter, c in crude} :
	sum{p in proc}io[mi,c,p] * LevPr[p,c] + (if mi in m_purch then InInt[mi,c]) >= sum{(mf,mi) in blend}LevBl[mf,mi,c];

s.t. C3 {mf in m_final} :
	Out[mf] = sum{(mf,mi) in blend, c in crude}LevBl[mf,mi,c];

s.t. C4 {mf in m_final, q in qual : attr_min[mf,q] != 0} :
	sum{mi in m_inter, c in crude : (mf,mi) in blend}attr[mi,c,q] * LevBl[mf,mi,c] >= attr_min[mf,q] * Out[mf];

s.t. C5 {mf in m_final, q in qual : attr_max[mf,q] != 0} :
	sum{mi in m_inter, c in crude : (mf,mi) in blend}attr[mi,c,q] * LevBl[mf,mi,c] <= attr_max[mf,q] * Out[mf];

s.t. C6 {u in unit} :
	sum{p in proc}(util[u,p] * sum{c in crude}LevPr[p,c]) <= cap[u];

s.t. C7 {c in crude} :
	InCr[c] <= purch_max[c];

s.t. C8 : Revenue = sum{mf in m_final}price[mf] * Out[mf];

s.t. C9 : PurchCost = sum{c in crude}price[c] * InCr[c] + sum{mp in m_purch, c in crude}price[mp] * InInt[mp,c];

s.t. C10 : OperCost = sum{p in proc}(cost[p] * sum{c in crude}LevPr[p,c]);


