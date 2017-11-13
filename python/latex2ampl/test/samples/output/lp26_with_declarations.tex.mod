param c, >= 0;

set SCENS;

param r, >= 0;

param w, >= 0;

param Pr{s in SCENS}, >= 0;

param D{s in SCENS}, >= 0;

param ExD, := sum{k in SCENS}Pr[k] * D[k];

param EVPI, := sum{k in SCENS}Pr[k] * (r - c) * D[k];

param EVM, := -c * ExD + sum{k in SCENS}Pr[k] * (r * min(ExD,D[k]) + w * max(ExD - D[k],0));


var x >= 0;

var ExProfit;

var y{k in SCENS} >= 0;


maximize obj: ExProfit;

s.t. C1  : ExProfit = -c * x + sum{k in SCENS}Pr[k] * (r * y[k] + w * (x - y[k]));

s.t. C2 {k in SCENS} :
	y[k] <= x;

s.t. C3 {k in SCENS} :
	y[k] <= D[k];


