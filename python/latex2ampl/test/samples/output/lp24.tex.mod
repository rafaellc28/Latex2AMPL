set CUSTOMERS dimen 2;

set FINISH dimen 2;

param Minspeed;

set P;

set LOCATIONS;

set N dimen 2;

set START dimen 2;

param Maxspeed;

param BigM;

param TS2{(a,aLoc) in START};

param T2{(a,aLoc) in CUSTOMERS};

param T1{(a,aLoc) in CUSTOMERS};

param Gcdist{a in LOCATIONS, b in LOCATIONS};

param TF2{(a,aLoc) in FINISH};

param TF1{(a,aLoc) in FINISH};

param TS1{(a,aLoc) in START};


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


minimize obj: 5 * timePenalty + totalDistance / Maxspeed;

s.t. C1 {p in P, (a,aLoc) in N, (b,bLoc) in START} :
	x[p,a,aLoc,b,bLoc] = 0;

s.t. C2 {p in P, (a,aLoc) in FINISH, (b,bLoc) in N} :
	x[p,a,aLoc,b,bLoc] = 0;

s.t. C3 {p in P, (a,aLoc) in START, (b,bLoc) in N : p <> a} :
	x[p,a,aLoc,b,bLoc] = 0;

s.t. C4 {p in P, (a,aLoc) in N, (b,bLoc) in FINISH : p <> b} :
	x[p,a,aLoc,b,bLoc] = 0;

s.t. C5 {(b,bLoc) in (CUSTOMERS union FINISH)} :
	sum{p in P, (a,aLoc) in (CUSTOMERS union START)}x[p,a,aLoc,b,bLoc] = 1;

s.t. C6 {(a,aLoc) in (START union CUSTOMERS)} :
	sum{p in P, (b,bLoc) in (CUSTOMERS union FINISH)}x[p,a,aLoc,b,bLoc] = 1;

s.t. C7 {p in P, (a,aLoc) in CUSTOMERS} :
	sum{(b,bLoc) in (CUSTOMERS union START)}x[p,b,bLoc,a,aLoc] = sum{(b,bLoc) in (CUSTOMERS union FINISH)}x[p,a,aLoc,b,bLoc];

s.t. C8 {p in P, (a,aLoc) in N, (b,bLoc) in N : (a = b) and (aLoc = bLoc)} :
	x[p,a,aLoc,b,bLoc] = 0;

s.t. C9  : sum{p in P, (a,aLoc) in START, (b,bLoc) in N}y[p,a,aLoc,b,bLoc] = card(CUSTOMERS);

s.t. C10 {(a,aLoc) in CUSTOMERS} :
	sum{p in P, (b,bLoc) in (CUSTOMERS union START)}y[p,b,bLoc,a,aLoc] = 1 + sum{p in P, (b,bLoc) in (CUSTOMERS union FINISH)}y[p,a,aLoc,b,bLoc];

s.t. C11 {(a,aLoc) in N} :
	tlv[a,aLoc] >= tar[a,aLoc];

s.t. C12 {p in P, (a,aLoc) in N, (b,bLoc) in N} :
	tar[b,bLoc] >= tlv[a,aLoc] + Gcdist[aLoc,bLoc] / Maxspeed - BigM * (1 - x[p,a,aLoc,b,bLoc]);

s.t. C13 {p in P, (a,aLoc) in N, (b,bLoc) in N} :
	tar[b,bLoc] <= tlv[a,aLoc] + Gcdist[aLoc,bLoc] / Minspeed + BigM * (1 - x[p,a,aLoc,b,bLoc]);

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
	routeDistance[p] = sum{(a,aLoc) in N, (b,bLoc) in N}Gcdist[aLoc,bLoc] * x[p,a,aLoc,b,bLoc];

s.t. C23  : totalDistance = sum{p in P}routeDistance[p];

s.t. C24  : timePenalty = sum{(a,aLoc) in N}(tea[a,aLoc] + 2 * tla[a,aLoc] + 2 * ted[a,aLoc] + tld[a,aLoc]);

s.t. C25 {p in P, (a,aLoc) in N, (b,bLoc) in N} :
	y[p,a,aLoc,b,bLoc] <= card(CUSTOMERS) * x[p,a,aLoc,b,bLoc];

s.t. C26 {a in LOCATIONS, b in LOCATIONS} :
	Gcdist[a,b] >= 0;

s.t. C27 {(a,aLoc) in N} :
	tlv[a,aLoc] >= 0;

s.t. C28 {(a,aLoc) in N} :
	tar[a,aLoc] >= 0;

s.t. C29 {(a,aLoc) in N} :
	tea[a,aLoc] >= 0;

s.t. C30 {(a,aLoc) in N} :
	tla[a,aLoc] >= 0;

s.t. C31 {(a,aLoc) in N} :
	ted[a,aLoc] >= 0;

s.t. C32 {(a,aLoc) in N} :
	tld[a,aLoc] >= 0;


