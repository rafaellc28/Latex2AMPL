set PRODUCTS;

set RAWMATERIALS;

param bigM;

param avail{r in RAWMATERIALS};

param rLength{r in RAWMATERIALS};

param pLength{p in PRODUCTS};

param demand{p in PRODUCTS};

set Q{p in PRODUCTS}, := 1..demand[p];

set S{r in RAWMATERIALS}, := 1..avail[r];


var u{r in RAWMATERIALS, s in S[r]} binary;

var y{p in PRODUCTS, q in Q[p], r in RAWMATERIALS, s in S[r]} binary;

var w{r in RAWMATERIALS, s in S[r]} >= 0;


minimize obj: sum{r in RAWMATERIALS, s in S[r]}rLength[r] * s * u[r,s];

s.t. C1 {p in PRODUCTS, q in Q[p]} :
	sum{r in RAWMATERIALS, s in S[r]}y[p,q,r,s], = 1;

s.t. C2 {p in PRODUCTS} :
	sum{q in Q[p], r in RAWMATERIALS, s in S[r]}y[p,q,r,s], = demand[p];

s.t. C3 {r in RAWMATERIALS, s in S[r]} :
	sum{p in PRODUCTS, q in Q[p]}pLength[p] * y[p,q,r,s] + w[r,s], = rLength[r];

s.t. C4 {r in RAWMATERIALS, s in S[r]} :
	bigM * u[r,s], >= sum{p in PRODUCTS, q in Q[p]}y[p,q,r,s];


solve;


data;

set PRODUCTS :=;

set RAWMATERIALS :=;

param bigM := 0;

param avail :=;

param rLength :=;

param pLength :=;

param demand :=;


end;
