set REACTIONS;

set SPECIES;

set ATOMS;

set RAWMATERIALS, within SPECIES;

param name{s in SPECIES} symbolic;

set PRODUCTS, within SPECIES;

param formula{s in SPECIES, a in ATOMS}, >= 0;

param amu{a in ATOMS}, >= 0;

param stoich{s in SPECIES, r in REACTIONS};

param mw{s in PRODUCTS}, := sum{a in ATOMS}amu[a] * formula[s,a];

set BYPRODUCTS, := (SPECIES diff RAWMATERIALS diff PRODUCTS);


var x{r in REACTIONS};

var n{s in SPECIES};


maximize obj: sum{s in PRODUCTS}mw[s] * n[s];

s.t. C1 {s in SPECIES} :
	n[s] = sum{r in REACTIONS}stoich[s,r] * x[r];

s.t. C2 {s in RAWMATERIALS} :
	sum{r in REACTIONS}n[s] <= 0;

s.t. C3 {s in SPECIES diff RAWMATERIALS} :
	sum{r in REACTIONS}n[s] >= 0;

s.t. C4 : sum{s in RAWMATERIALS}-n[s] <= 1;


