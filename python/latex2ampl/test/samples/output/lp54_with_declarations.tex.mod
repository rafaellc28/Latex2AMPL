set cRaw;

set center;

param utilPct, := 0.85;

set cInter;

set region;

set nutr;

param exch, := 0.4;

set proc;

set unit;

set cFinal;

param pR{cr in cRaw}, >= 0;

set plant, within center;

set cShip, within cInter;

param util{u in unit, p in proc}, >= 0;

param road{r in region, c in center}, >= 0;

set commod, := cFinal union cInter union cRaw;

set port, within center;

param fn{cf in cFinal, n in nutr}, >= 0;

param cf75{r in region, cf in cFinal}, >= 0;

param impdBarg{p in plant}, >= 0;

param pImp{c in commod}, >= 0;

param tranFinal{pl in plant, r in region}, := if road[r,pl] > 0 then .5 + .0144 * road[r,pl];

param tranImport{r in region, po in port}, := if road[r,po] > 0 then .5 + .0144 * road[r,po];

param dcap{p in plant, u in unit}, >= 0;

param pPr{p in plant, cr in cRaw}, >= 0;

param railHalf{p1 in plant, p2 in plant}, >= 0;

param impdRoad{p in plant}, >= 0;

param io{c in commod, p in proc};

param cn75{r in region, n in nutr}, := sum{c in cFinal}cf75[r,c] * fn[c,n];

set pExcept{p in plant}, within proc;

param pDom{pl in plant, c in cRaw}, := if pR[c] > 0 then pR[c] else pPr[pl,c];

param tranRaw{pl in plant}, := (if impdBarg[pl] > 0 then 1.0 + .0030 * impdBarg[pl]) + (if impdRoad[pl] > 0 then 0.5 + .0144 * impdRoad[pl]);

param rail{p1 in plant, p2 in plant}, := if railHalf[p1,p2] > 0 then railHalf[p1,p2] else railHalf[p2,p1];

param icap{u in unit, pl in plant}, := 0.33 * dcap[pl,u];

set mPos{pl in plant}, := {u in unit : icap[u,pl] > 0};

param tranInter{p1 in plant, p2 in plant}, := if rail[p1,p2] > 0 then 3.5 + .03 * rail[p1,p2];

set pCap{pl in plant}, := {pr in proc : forall{u in unit : util[u,pr] > 0} u in mPos[pl]};

set pPos{pl in plant}, := pCap[pl] diff pExcept[pl];

set ccPos{c in commod}, := {pl in plant : sum{pr in pPos[pl]}io[c,pr] < 0};

set cpPos{c in commod}, := {pl in plant : sum{pr in pPos[pl]}io[c,pr] > 0};

set cPos{c in commod}, := cpPos[c] union ccPos[c];


var Psil;

var Psii;

var Psip;

var Xi{c in cShip, p1 in cpPos[c], p2 in ccPos[c]} >= 0;

var Vf{c in cFinal, r in region, po in port} >= 0;

var Xf{c in cFinal, pl in cpPos[c], r in region} >= 0;

var Vr{c in cRaw, pl in ccPos[c]} >= 0;

var U{c in cRaw, pl in ccPos[c]} >= 0;

var Z{pl in plant, pr in pPos[pl]} >= 0;


minimize obj: Psip + Psil + Psii;

s.t. C1 {n in nutr, r in region} :
	sum{c in cFinal}fn[c,n] * (sum{po in port}Vf[c,r,po] + sum{pl in cpPos[c]}Xf[c,pl,r]) >= cn75[r,n];

s.t. C2 {c in cFinal, r in region : cf75[r,c] > 0} :
	sum{po in port}Vf[c,r,po] + sum{pl in cpPos[c]}Xf[c,pl,r] >= cf75[r,c];

s.t. C3 {c in commod, pl in plant} :
	sum{pr in pPos[pl]}io[c,pr] * Z[pl,pr] + (if c in cShip then (if pl in cpPos[c] then sum{p2 in ccPos[c]}Xi[c,pl,p2]) - (if pl in ccPos[c] then sum{p2 in cpPos[c]}Xi[c,p2,pl])) + (if c in cRaw and pl in ccPos[c] then ((if pImp[c] > 0 then Vr[c,pl]) + (if pDom[pl,c] > 0 then U[c,pl]))) >= if c in cFinal and pl in cpPos[c] then sum{r in region}Xf[c,pl,r];

s.t. C4 {pl in plant, u in mPos[pl]} :
	sum{pr in pPos[pl]}util[u,pr] * Z[pl,pr] <= utilPct * icap[u,pl];

s.t. C5  : Psip = sum{c in cRaw, pl in ccPos[c]}pDom[pl,c] * U[c,pl];

s.t. C6  : Psil = sum{c in cFinal}(sum{pl in cpPos[c], r in region}tranFinal[pl,r] * Xf[c,pl,r] + sum{po in port, r in region}tranImport[r,po] * Vf[c,r,po]) + sum{c in cShip, p1 in cpPos[c], p2 in ccPos[c]}tranInter[p1,p2] * Xi[c,p1,p2] + sum{c in cRaw, pl in ccPos[c] : pImp[c] > 0}tranRaw[pl] * Vr[c,pl];

s.t. C7  : Psii / exch = sum{c in cFinal, r in region, po in port}pImp[c] * Vf[c,r,po] + sum{c in cRaw, pl in ccPos[c]}pImp[c] * Vr[c,pl];


