param R;

param C;

set SCENS;

param W;

param Pr{k in SCENS};

param D{k in SCENS};


var ExProfit;

var x >= 0;

var y{k in SCENS} >= 0;


maximize obj: ExProfit;

s.t. C1  : ExProfit, = -C * x + sum{k in SCENS}Pr[k] * (R * y[k] + W * (x - y[k]));

s.t. C2 {k in SCENS} :
	y[k], <= x;

s.t. C3 {k in SCENS} :
	y[k], <= D[k];


solve;


data;

param R := 0;

param C := 0;

set SCENS :=;

param W := 0;

param Pr :=;

param D :=;


end;
