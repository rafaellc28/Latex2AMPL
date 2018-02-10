param Start symbolic;

param Finish symbolic;

param BigM;

set PLACES;

param Maxspeed;

param S2{a in PLACES};

param S1{a in PLACES};

param Gcdist{a in PLACES, b in PLACES};


var Tmax >= 0;

var tlv{a in PLACES};

var tar{a in PLACES};

var tea{a in PLACES} >= 0;

var ted{a in PLACES} >= 0;

var tla{a in PLACES} >= 0;

var tld{a in PLACES} >= 0;

var y{a in PLACES, b in PLACES} integer >= 0;

var x{a in PLACES, b in PLACES} binary;


minimize obj: sum{a in PLACES}(1 * tea[a] + 2 * tla[a] + 2 * ted[a] + 1 * tld[a]) + 2 * Tmax;

s.t. C1 {a in PLACES : a != Finish} :
	sum{b in PLACES}x[a,b] = 1;

s.t. C2 : sum{b in PLACES}x[Finish,b] = 0;

s.t. C3 {a in PLACES : a != Start} :
	sum{b in PLACES}x[b,a] = 1;

s.t. C4 : sum{b in PLACES}x[b,Start] = 0;

s.t. C5 {a in PLACES, b in PLACES} :
	y[a,b] <= (card(PLACES) - 1) * x[a,b];

s.t. C6 {a in PLACES} :
	sum{b in PLACES}y[b,a] + (if a = Start then card(PLACES)) = 1 + sum{b in PLACES}y[a,b];

s.t. C7 {a in PLACES} :
	tlv[a] >= tar[a];

s.t. C8 {a in PLACES, b in PLACES} :
	tar[b] >= tlv[a] + Gcdist[a,b] / Maxspeed - BigM * (1 - x[a,b]);

s.t. C9 {a in PLACES : a != Start} :
	tea[a] >= S1[a] - tar[a];

s.t. C10 {a in PLACES : a != Start} :
	tla[a] >= tar[a] - S2[a];

s.t. C11 {a in PLACES : a != Finish} :
	ted[a] >= S1[a] - tlv[a];

s.t. C12 {a in PLACES : a != Finish} :
	tld[a] >= tlv[a] - S2[a];

s.t. C13 {a in PLACES} :
	tea[a] <= Tmax;

s.t. C14 {a in PLACES} :
	tla[a] <= Tmax;

s.t. C15 {a in PLACES} :
	ted[a] <= Tmax;

s.t. C16 {a in PLACES} :
	tld[a] <= Tmax;


