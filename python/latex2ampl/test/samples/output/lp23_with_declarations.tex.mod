set CUSTOMERS dimen 2;

param d2r, := 3.1415926 / 180;

set LOCATIONS;

set PLANES dimen 3;

param lat{l in LOCATIONS};

set START dimen 2, := setof {(p,sLoc,fLoc) in PLANES} (p,sLoc);

param lng{l in LOCATIONS};

set FINISH dimen 2, := setof {(p,sLoc,fLoc) in PLANES} (p,fLoc);

set P, := setof {(p,sLoc,fLoc) in PLANES} p;

param alpha{a in LOCATIONS, b in LOCATIONS}, := sin(d2r * (lat[a] - lat[b]) / 2) ^ 2 + cos(d2r * lat[a]) * cos(d2r * lat[b]) * sin(d2r * (lng[a] - lng[b]) / 2) ^ 2;

set N dimen 2, := CUSTOMERS union (START union FINISH);

param gcdist{a in LOCATIONS, b in LOCATIONS}, := 2 * 6371 * atan2(sqrt(alpha[a,b]), sqrt(1 - alpha[a,b]));


var maxDistance >= 0;

var maxLegs >= 0;

var y{p in P, (a,aLoc) in N, (b,bLoc) in N} integer >= 0;

var x{p in P, (a,aLoc) in N, (b,bLoc) in N} binary;

var routeDistance{p in P} >= 0;

var routeLegs{p in P} >= 0;


minimize obj: sum{p in P}routeDistance[p];

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

s.t. C9 {p in P, (a,aLoc) in N, (b,bLoc) in N} :
	y[p,a,aLoc,b,bLoc] <= card(CUSTOMERS) * x[p,a,aLoc,b,bLoc];

s.t. C10 : sum{p in P, (a,aLoc) in START, (b,bLoc) in N}y[p,a,aLoc,b,bLoc] = card(CUSTOMERS);

s.t. C11 {(a,aLoc) in CUSTOMERS} :
	sum{p in P, (b,bLoc) in (CUSTOMERS union START)}y[p,b,bLoc,a,aLoc] = 1 + sum{p in P, (b,bLoc) in (CUSTOMERS union FINISH)}y[p,a,aLoc,b,bLoc];

s.t. C12 {p in P} :
	routeDistance[p] = sum{(a,aLoc) in N, (b,bLoc) in N}gcdist[aLoc,bLoc] * x[p,a,aLoc,b,bLoc];

s.t. C13 {p in P} :
	routeLegs[p] = sum{(a,aLoc) in START, (b,bLoc) in N}y[p,a,aLoc,b,bLoc];

s.t. C14 {p in P} :
	routeDistance[p] <= maxDistance;

s.t. C15 {p in P} :
	routeLegs[p] <= maxLegs;


