set rt dimen 2;

param otmax;

set dctr;

param rtmin;

param rtmax;

param otmin;

set prod;

set whse;

set fact;

param rpc{p in prod, f in fact};

param rmin{f in fact};

param pt{p in prod, f in fact};

param hd{f in fact};

param tc{p in prod};

param rmax{f in fact};

param wt{p in prod};

param opc{p in prod, f in fact};

param dp{f in fact};

param omin{f in fact};

param dem{p in prod, w in whse};

param sc{(d,w) in rt};

param omax{f in fact};


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


