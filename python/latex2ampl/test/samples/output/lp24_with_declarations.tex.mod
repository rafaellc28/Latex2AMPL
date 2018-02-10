set CUSTOMERS dimen 2;

param maxspeed, > 0;

param d2r, := 3.1415926 / 180;

set LOCATIONS;

set PLANES dimen 3;

param bigM, := 50;

param F1{(p,sLoc,fLoc) in PLANES};

set FINISH dimen 2, := setof {(p,sLoc,fLoc) in PLANES} (p,fLoc);

param minspeed, <= maxspeed, > 0;

set P, := setof {(p,sLoc,fLoc) in PLANES} p;

param S1{(p,sLoc,fLoc) in PLANES};

param T1{(name,loc) in CUSTOMERS};

set START dimen 2, := setof {(p,sLoc,fLoc) in PLANES} (p,sLoc);

param lat{l in LOCATIONS};

param lng{l in LOCATIONS};

param F2{(p,sLoc,fLoc) in PLANES}, >= F1[p,sLoc,fLoc];

param S2{(p,sLoc,fLoc) in PLANES}, >= S1[p,sLoc,fLoc];

param T2{(name,loc) in CUSTOMERS}, >= T1[name,loc];

set N dimen 2, := CUSTOMERS union (START union FINISH);

param alpha{a in LOCATIONS, b in LOCATIONS}, := sin(d2r * (lat[a] - lat[b]) / 2) ^ 2 + cos(d2r * lat[a]) * cos(d2r * lat[b]) * sin(d2r * (lng[a] - lng[b]) / 2) ^ 2;

param TF1{(p,fLoc) in FINISH}, := max{(q,sLoc,gLoc) in PLANES : (p = q) and (fLoc = gLoc)}F1[p,sLoc,fLoc];

param TS1{(p,sLoc) in START}, := max{(q,tLoc,fLoc) in PLANES : (p = q) and (sLoc = tLoc)}S1[p,sLoc,fLoc];

param TS2{(p,sLoc) in START}, := min{(q,tLoc,fLoc) in PLANES : (p = q) and (sLoc = tLoc)}S2[p,sLoc,fLoc];

param gcdist{a in LOCATIONS, b in LOCATIONS}, := 2 * 6371 * atan2(sqrt(alpha[a,b]), sqrt(1 - alpha[a,b]));

param TF2{(p,fLoc) in FINISH}, := min{(q,sLoc,gLoc) in PLANES : (p = q) and (fLoc = gLoc)}F2[p,sLoc,fLoc];


var timePenalty >= 0;

var totalDistance >= 0;

var routeDistance{p in P} >= 0;

var tlv{(a,aLoc) in N};

var tar{(a,aLoc) in N};

var tea{(a,aLoc) in N} >= 0;

var ted{(a,aLoc) in N} >= 0;

var tla{(a,aLoc) in N} >= 0;

var tld{(a,aLoc) in N} >= 0;

var y{p in P, (a,aLoc) in N, (b,bLoc) in N} >= 0;

var x{p in P, (a,aLoc) in N, (b,bLoc) in N} binary;


minimize obj: 5 * timePenalty + totalDistance / maxspeed;

s.t. C1 {p in P, (a,aLoc) in N, (b,bLoc) in START} :
	x[p,a,aLoc,b,bLoc] = 0;

s.t. C2 {p in P, (a,aLoc) in FINISH, (b,bLoc) in N} :
	x[p,a,aLoc,b,bLoc] = 0;

s.t. C3 {p in P, (a,aLoc) in START, (b,bLoc) in N : p != a} :
	x[p,a,aLoc,b,bLoc] = 0;

s.t. C4 {p in P, (a,aLoc) in N, (b,bLoc) in FINISH : p != b} :
	x[p,a,aLoc,b,bLoc] = 0;

s.t. C5 {(b,bLoc) in (CUSTOMERS union FINISH)} :
	sum{p in P, (a,aLoc) in (CUSTOMERS union START)}x[p,a,aLoc,b,bLoc] = 1;

s.t. C6 {(a,aLoc) in (START union CUSTOMERS)} :
	sum{p in P, (b,bLoc) in (CUSTOMERS union FINISH)}x[p,a,aLoc,b,bLoc] = 1;

s.t. C7 {p in P, (a,aLoc) in CUSTOMERS} :
	sum{(b,bLoc) in (CUSTOMERS union START)}x[p,b,bLoc,a,aLoc] = sum{(b,bLoc) in (CUSTOMERS union FINISH)}x[p,a,aLoc,b,bLoc];

s.t. C8 {p in P, (a,aLoc) in N, (b,bLoc) in N : (a = b) and (aLoc = bLoc)} :
	x[p,a,aLoc,b,bLoc] = 0;

s.t. C9 : sum{p in P, (a,aLoc) in START, (b,bLoc) in N}y[p,a,aLoc,b,bLoc] = card(CUSTOMERS);

s.t. C10 {(a,aLoc) in CUSTOMERS} :
	sum{p in P, (b,bLoc) in (CUSTOMERS union START)}y[p,b,bLoc,a,aLoc] = 1 + sum{p in P, (b,bLoc) in (CUSTOMERS union FINISH)}y[p,a,aLoc,b,bLoc];

s.t. C11 {(a,aLoc) in N} :
	tlv[a,aLoc] >= tar[a,aLoc];

s.t. C12 {p in P, (a,aLoc) in N, (b,bLoc) in N} :
	tar[b,bLoc] >= tlv[a,aLoc] + gcdist[aLoc,bLoc] / maxspeed - bigM * (1 - x[p,a,aLoc,b,bLoc]);

s.t. C13 {p in P, (a,aLoc) in N, (b,bLoc) in N} :
	tar[b,bLoc] <= tlv[a,aLoc] + gcdist[aLoc,bLoc] / minspeed + bigM * (1 - x[p,a,aLoc,b,bLoc]);

s.t. C14 {(a,aLoc) in CUSTOMERS} :
	tea[a,aLoc] >= T1[a,aLoc] - tar[a,aLoc];

s.t. C15 {(a,aLoc) in FINISH} :
	tea[a,aLoc] >= TF1[a,aLoc] - tar[a,aLoc];

s.t. C16 {(a,aLoc) in CUSTOMERS} :
	tla[a,aLoc] >= tar[a,aLoc] - T2[a,aLoc];

s.t. C17 {(a,aLoc) in FINISH} :
	tla[a,aLoc] >= tar[a,aLoc] - TF2[a,aLoc];

s.t. C18 {(a,aLoc) in START} :
	ted[a,aLoc] >= TS1[a,aLoc] - tlv[a,aLoc];

s.t. C19 {(a,aLoc) in CUSTOMERS} :
	ted[a,aLoc] >= T1[a,aLoc] - tlv[a,aLoc];

s.t. C20 {(a,aLoc) in START} :
	tld[a,aLoc] >= tlv[a,aLoc] - TS2[a,aLoc];

s.t. C21 {(a,aLoc) in CUSTOMERS} :
	tld[a,aLoc] >= tlv[a,aLoc] - T2[a,aLoc];

s.t. C22 {p in P} :
	routeDistance[p] = sum{(a,aLoc) in N, (b,bLoc) in N}gcdist[aLoc,bLoc] * x[p,a,aLoc,b,bLoc];

s.t. C23 : totalDistance = sum{p in P}routeDistance[p];

s.t. C24 : timePenalty = sum{(a,aLoc) in N}(tea[a,aLoc] + 2 * tla[a,aLoc] + 2 * ted[a,aLoc] + tld[a,aLoc]);

s.t. C25 {p in P, (a,aLoc) in N, (b,bLoc) in N} :
	y[p,a,aLoc,b,bLoc] <= card(CUSTOMERS) * x[p,a,aLoc,b,bLoc];


