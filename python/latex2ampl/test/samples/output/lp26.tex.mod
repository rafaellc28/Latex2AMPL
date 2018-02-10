param R;

param C;

set SCENS;

param W;

param Pr{k in SCENS};

param D{k in SCENS};


var x >= 0;

var ExProfit;

var y{k in SCENS} >= 0;


maximize obj: ExProfit;

s.t. C1 : ExProfit = -C * x + sum{k in SCENS}Pr[k] * (R * y[k] + W * (x - y[k]));

s.t. C2 {k in SCENS} :
	y[k] <= x;

s.t. C3 {k in SCENS} :
	y[k] <= D[k];


