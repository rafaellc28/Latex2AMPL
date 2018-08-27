set rt dimen 2;

param huge, > 0;

param otmax;

set dctr;

param rtmin, >= 0;

param rtmax;

param otmin, >= 0;

set prod;

set whse;

set fact;

param rmin{f in fact}, >= 0;

param sc{d in dctr, w in whse}, >= 0;

param pt{p in prod, f in fact}, >= 0;

param rmax{f in fact};

param dsr{d in dctr}, >= 0;

param msr{d in dctr, w in whse};

param tc{p in prod}, >= 0;

param omin{f in fact}, >= 0;

param rpc{p in prod, f in fact}, >= 0;

param wt{p in prod}, > 0;

param hd{f in fact}, >= 0;

param opc{p in prod, f in fact}, >= 0;

param cpp{p in prod}, > 0;

param dt{p in prod}, >= 0;

param ds{p in prod, w in whse}, >= 0;

param dp{f in fact}, > 0;

param omax{f in fact};

param dstot{p in prod}, := sum{w in whse}ds[p,w];

param dem{p in prod, w in whse}, := dt[p] * ds[p,w]/dstot[p];


var Oprod{p in prod, f in fact}, >= 0;

var Ship{p in prod, (v,w) in rt}, >= 0;

var Trans{p in prod, d in dctr}, >= 0;

var Rprod{p in prod, f in fact}, >= 0;


minimize obj: sum{p in prod, f in fact}rpc[p,f] * Rprod[p,f] + sum{p in prod, f in fact}opc[p,f] * Oprod[p,f] + sum{p in prod, (d,w) in rt}sc[d,w] * wt[p] * Ship[p,d,w] + sum{p in prod, d in dctr}tc[p] * Trans[p,d];

s.t. C1 : rtmin <= sum{p in prod, f in fact}(pt[p,f] * Rprod[p,f])/(dp[f] * hd[f]) <= rtmax;

s.t. C2 : otmin <= sum{p in prod, f in fact}pt[p,f] * Oprod[p,f] <= otmax;

s.t. C3 {f in fact} :
	rmin[f] <= sum{p in prod}(pt[p,f] * Rprod[p,f])/(dp[f] * hd[f]) <= rmax[f];

s.t. C4 {f in fact} :
	omin[f] <= sum{p in prod}pt[p,f] * Oprod[p,f] <= omax[f];

s.t. C5 {p in prod, w in whse} :
	sum{(v,w) in rt}Ship[p,v,w] + (if w in fact then Rprod[p,w] + Oprod[p,w]) = dem[p,w] + (if w in dctr then sum{(w,v) in rt}Ship[p,w,v]);

s.t. C6 {p in prod, d in dctr} :
	Trans[p,d] >= sum{(d,w) in rt}Ship[p,d,w] - (if d in fact then Rprod[p,d] + Oprod[p,d]);


