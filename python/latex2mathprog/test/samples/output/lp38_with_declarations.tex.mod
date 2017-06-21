set CONTRACTS dimen 2;

param payout{(m,e) in CONTRACTS};

param price{(m,e) in CONTRACTS};

set MARKETS, := setof {(m,e) in CONTRACTS} m;

set EVENTS, := setof {(m,e) in CONTRACTS} e;


var minpayout >= 0;

var x{m in MARKETS, e in EVENTS} >= 0;


maximize obj: minpayout;

s.t. C1  : sum{(m,e) in CONTRACTS}price[m,e] * x[m,e], <= 1000;

s.t. C2 {e in EVENTS} :
	sum{m in MARKETS}payout[m,e] * x[m,e], >= minpayout;


solve;


data;

set CONTRACTS :=;

param payout :=;

param price :=;


end;
