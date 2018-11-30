param huge, > 0;

param rtmin, >= 0;

param otmin, >= 0;

set prod;

set whse;

param dt{p in prod}, >= 0;

param rtmax, >= rtmin;

param otmax, >= otmin;

set dctr, within whse;

param tc{p in prod}, >= 0;

param dsr{d in dctr}, >= 0;

param msr{d in dctr, w in whse} logical;

param sc{d in dctr, w in whse}, >= 0;

set fact, within dctr;

param pt{p in prod, f in fact}, >= 0;

param omin{f in fact}, >= 0;

param rmin{f in fact}, >= 0;

param rpc{p in prod, f in fact}, >= 0;

param wt{p in prod}, > 0;

param dp{f in fact}, > 0;

param opc{p in prod, f in fact}, >= 0;

param cpp{p in prod}, > 0;

param ds{p in prod, w in whse}, <= 1, >= 0;

param hd{f in fact}, >= 0;

param rmax{f in fact}, >= rmin[f];

param dstot{p in prod}, := sum{w in whse}ds[p,w];

param omax{f in fact}, >= omin[f];

param dem{p in prod, w in whse}, := dt[p] * ds[p,w]/dstot[p];

set rt dimen 2, := {d in dctr, w in whse : d != w and sc[d,w] < huge and (w in dctr or sum{p in prod}dem[p,w] > 0) and not (msr[d,w] and sum{p in prod}1000 * dem[p,w]/cpp[p] < dsr[d])};


minimize cost: to_come;

node RT : rtmin <= net_out <= rtmax;

node OT : otmin <= net_out <= otmax;

node P_RT {f in fact};

node P_OT {f in fact};

node M {p in prod, f in fact};

node D {p in prod, d in dctr};

node W {p in prod, w in whse} :
	net_in = dem[p,w];

arc Work_RT {f in fact} >= rmin[f], <= rmax[f],
	 from RT, to P_RT[f];

arc Work_OT {f in fact} >= omin[f], <= omax[f],
	 from OT, to P_OT[f];

arc Manu_RT {p in prod, f in fact : rpc[p,f] != 0} >= 0,
	 from P_RT[f], to M[p,f] ((dp[f] * hd[f])/pt[p,f]), obj cost ((rpc[p,f] * dp[f] * hd[f])/pt[p,f]);

arc Manu_OT {p in prod, f in fact : opc[p,f] != 0} >= 0,
	 from P_OT[f], to M[p,f] (1/pt[p,f]), obj cost (opc[p,f]/pt[p,f]);

arc Prod_L {p in prod, f in fact} >= 0,
	 from M[p,f], to W[p,f];

arc Prod_D {p in prod, f in fact} >= 0,
	 from M[p,f], to D[p,f];

arc Ship {p in prod, (d,w) in rt} >= 0,
	 from D[p,d], to W[p,w], obj cost (sc[d,w] * wt[p]);

arc Trans {p in prod, d in dctr} >= 0,
	 from W[p,d], to D[p,d], obj cost (tc[p]);


