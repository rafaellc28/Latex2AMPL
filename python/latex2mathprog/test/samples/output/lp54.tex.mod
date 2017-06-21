set plant;

set cRaw;

set cShip;

param UtilPct;

set region;

set nutr;

param Exch;

set commod;

set proc;

set port;

set unit;

set cFinal;

param PDom{pl in plant, r in cRaw};

param TranInter{p1 in plant, p2 in plant};

param TranRaw{pl in plant};

param PImp{c in commod};

set mPos{pl in plant};

set cpPos{c in commod};

param TranFinal{pl in plant, r in region};

param TranImport{r in region, po in port};

param Icap{u in unit, pl in plant};

param Util{u in unit, p in proc};

param Io{c in commod, p in proc};

param Cn75{r in region, n in nutr};

set ccPos{c in commod};

set pPos{pl in plant};

param Fn{c in cFinal, n in nutr};

param Cf75{r in region, c in cFinal};


var Psip;

var Psil;

var Psii;

var Xf{c in cFinal, pl in cpPos[c], r in region} >= 0;

var Vf{c in cFinal, r in region, po in port} >= 0;

var Z{pl in plant, pr in pPos[pl]} >= 0;

var Xi{c in cShip, p1 in cpPos[c], p2 in ccPos[c]} >= 0;

var Vr{c in cRaw, pl in ccPos[c]} >= 0;

var U{c in cRaw, pl in ccPos[c]} >= 0;


minimize obj: Psip + Psil + Psii;

s.t. C1 {n in nutr, r in region} :
	sum{c in cFinal}Fn[c,n] * (sum{po in port}Vf[c,r,po] + sum{pl in cpPos[c]}Xf[c,pl,r]), >= Cn75[r,n];

s.t. C2 {c in cFinal, r in region : Cf75[r,c] > 0} :
	sum{po in port}Vf[c,r,po] + sum{pl in cpPos[c]}Xf[c,pl,r], >= Cf75[r,c];

s.t. C3 {c in commod, pl in plant} :
	sum{pr in pPos[pl]}Io[c,pr] * Z[pl,pr] + (if c in cShip then (if pl in cpPos[c] then sum{p2 in ccPos[c]}Xi[c,pl,p2] else 0) - (if pl in ccPos[c] then sum{p2 in cpPos[c]}Xi[c,p2,pl] else 0) else 0) + (if c in cRaw and pl in ccPos[c] then ((if PImp[c] > 0 then Vr[c,pl] else 0) + (if PDom[pl,c] > 0 then U[c,pl] else 0)) else 0), >= if c in cFinal and pl in cpPos[c] then sum{r in region}Xf[c,pl,r] else 0;

s.t. C4 {pl in plant, u in mPos[pl]} :
	sum{pr in pPos[pl]}Util[u,pr] * Z[pl,pr], <= UtilPct * Icap[u,pl];

s.t. C5  : Psip, = sum{c in cRaw, pl in ccPos[c]}PDom[pl,c] * U[c,pl];

s.t. C6  : Psil, = sum{c in cFinal}(sum{pl in cpPos[c], r in region}TranFinal[pl,r] * Xf[c,pl,r] + sum{po in port, r in region}TranImport[r,po] * Vf[c,r,po]) + sum{c in cShip, p1 in cpPos[c], p2 in ccPos[c]}TranInter[p1,p2] * Xi[c,p1,p2] + sum{c in cRaw, pl in ccPos[c] : PImp[c] > 0}TranRaw[pl] * Vr[c,pl];

s.t. C7  : Psii / Exch, = sum{c in cFinal, r in region, po in port}PImp[c] * Vf[c,r,po] + sum{c in cRaw, pl in ccPos[c]}PImp[c] * Vr[c,pl];

s.t. C8 {pl in plant} :
	TranRaw[pl], >= 0;

s.t. C9 {p1 in plant, p2 in plant} :
	TranInter[p1,p2], >= 0;

s.t. C10 {pl in plant, r in region} :
	TranFinal[pl,r], >= 0;

s.t. C11 {u in unit, p in proc} :
	Util[u,p], >= 0;

s.t. C12 {c in commod, p in proc} :
	Io[c,p], <= 1;

s.t. C13 {u in unit, pl in plant} :
	Icap[u,pl], >= 0;

s.t. C14 {pl in plant, r in cRaw} :
	PDom[pl,r], >= 0;

s.t. C15 {c in commod} :
	PImp[c], >= 0;

s.t. C16 {c in commod} :
	sum{pl in cpPos[c]}1, >= 0;

s.t. C17 {c in commod} :
	sum{pl in ccPos[c]}1, >= 0;


solve;


data;

set plant :=;

set cRaw :=;

set cShip :=;

param UtilPct := 0;

set region :=;

set nutr :=;

param Exch := 0;

set commod :=;

set proc :=;

set port :=;

set unit :=;

set cFinal :=;

param PDom :=;

param TranInter :=;

param TranRaw :=;

param PImp :=;

set mPos[0] :=;

set cpPos[0] :=;

param TranFinal :=;

param TranImport :=;

param Icap :=;

param Util :=;

param Io :=;

param Cn75 :=;

set ccPos[0] :=;

set pPos[0] :=;

param Fn :=;

param Cf75 :=;


end;
