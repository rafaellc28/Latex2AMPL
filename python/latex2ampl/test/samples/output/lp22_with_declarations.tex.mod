param start symbolic;

param maxspeed;

param d2r, := 3.1415926 / 180;

set PLACES;

param bigM, := 50;

param lat{p in PLACES};

param S1{p in PLACES};

param finish symbolic, != start;

param lng{p in PLACES};

param S2{p in PLACES}, >= S1[p];

param alpha{a in PLACES, b in PLACES}, := sin(d2r * (lat[a] - lat[b]) / 2) ^ 2 + cos(d2r * lat[a]) * cos(d2r * lat[b]) * sin(d2r * (lng[a] - lng[b]) / 2) ^ 2;

param gcdist{a in PLACES, b in PLACES}, := 2 * 6371 * atan2(sqrt(alpha[a,b]), sqrt(1 - alpha[a,b]));


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

s.t. C1 {a in PLACES : a <> finish} :
	sum{b in PLACES}x[a,b] = 1;

s.t. C2  : sum{b in PLACES}x[finish,b] = 0;

s.t. C3 {a in PLACES : a <> start} :
	sum{b in PLACES}x[b,a] = 1;

s.t. C4  : sum{b in PLACES}x[b,start] = 0;

s.t. C5 {a in PLACES, b in PLACES} :
	y[a,b] <= (card(PLACES) - 1) * x[a,b];

s.t. C6 {a in PLACES} :
	sum{b in PLACES}y[b,a] + (if a = start then card(PLACES) else 0) = 1 + sum{b in PLACES}y[a,b];

s.t. C7 {a in PLACES} :
	tlv[a] >= tar[a];

s.t. C8 {a in PLACES, b in PLACES} :
	tar[b] >= tlv[a] + gcdist[a,b] / maxspeed - bigM * (1 - x[a,b]);

s.t. C9 {a in PLACES : a <> start} :
	tea[a] >= S1[a] - tar[a];

s.t. C10 {a in PLACES : a <> start} :
	tla[a] >= tar[a] - S2[a];

s.t. C11 {a in PLACES : a <> finish} :
	ted[a] >= S1[a] - tlv[a];

s.t. C12 {a in PLACES : a <> finish} :
	tld[a] >= tlv[a] - S2[a];

s.t. C13 {a in PLACES} :
	tea[a] <= Tmax;

s.t. C14 {a in PLACES} :
	tla[a] <= Tmax;

s.t. C15 {a in PLACES} :
	ted[a] <= Tmax;

s.t. C16 {a in PLACES} :
	tld[a] <= Tmax;


