set REACTIONS;

set PRODUCTS;

set RAWMATERIALS;

set SPECIES;

param MW{s in PRODUCTS};

param Stoich{s in SPECIES, r in REACTIONS};


var x{r in REACTIONS};

var n{s in SPECIES};


maximize obj: sum{s in PRODUCTS}MW[s] * n[s];

s.t. C1 {s in SPECIES} :
	n[s] = sum{r in REACTIONS}Stoich[s,r] * x[r];

s.t. C2 {s in RAWMATERIALS} :
	sum{r in REACTIONS}n[s] <= 0;

s.t. C3 {s in SPECIES diff RAWMATERIALS} :
	sum{r in REACTIONS}n[s] >= 0;

s.t. C4 : sum{s in RAWMATERIALS}-n[s] <= 1;

s.t. C5 {s in SPECIES} :
	n[s] <= 1;


