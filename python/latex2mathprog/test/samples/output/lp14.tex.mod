set SOURCES;

set CUSTOMERS;

param Supply{s in SOURCES};

param Tcost{c in CUSTOMERS, s in SOURCES};

param Demand{c in CUSTOMERS};


var x{c in CUSTOMERS, s in SOURCES} >= 0;


minimize obj: sum{c in CUSTOMERS, s in SOURCES}Tcost[c,s] * x[c,s];

s.t. C1 {s in SOURCES} :
	sum{c in CUSTOMERS}x[c,s], <= Supply[s];

s.t. C2 {c in CUSTOMERS} :
	sum{s in SOURCES}x[c,s], = Demand[c];


solve;


data;

set SOURCES :=;

set CUSTOMERS :=;

param Supply :=;

param Tcost :=;

param Demand :=;


end;
