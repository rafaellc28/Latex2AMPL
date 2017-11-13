set RAWMATERIALS;

set PRODUCTS;

param BigM;

set Q{p in PRODUCTS};

param RLength{r in RAWMATERIALS};

set S{r in RAWMATERIALS};

param PLength{p in PRODUCTS};

param Demand{p in PRODUCTS};


var y{p in PRODUCTS, q in Q[p], r in RAWMATERIALS, s in S[r]} binary;

var u{r in RAWMATERIALS, s in S[r]} binary;

var w{r in RAWMATERIALS, s in S[r]} >= 0;


minimize obj: sum{r in RAWMATERIALS, s in S[r]}RLength[r] * s * u[r,s];

s.t. C1 {p in PRODUCTS, q in Q[p]} :
	sum{r in RAWMATERIALS, s in S[r]}y[p,q,r,s] = 1;

s.t. C2 {p in PRODUCTS} :
	sum{q in Q[p], r in RAWMATERIALS, s in S[r]}y[p,q,r,s] = Demand[p];

s.t. C3 {r in RAWMATERIALS, s in S[r]} :
	sum{p in PRODUCTS, q in Q[p]}PLength[p] * y[p,q,r,s] + w[r,s] = RLength[r];

s.t. C4 {r in RAWMATERIALS, s in S[r]} :
	BigM * u[r,s] >= sum{p in PRODUCTS, q in Q[p]}y[p,q,r,s];


