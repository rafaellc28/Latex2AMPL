set CONTRACTS dimen 2;

set MARKETS;

set EVENTS;

param Payout{m in MARKETS, e in EVENTS};

param Price{(m,e) in CONTRACTS};


var minpayout >= 0;

var x{m in MARKETS, e in EVENTS} >= 0;


maximize obj: minpayout;

s.t. C1 : sum{(m,e) in CONTRACTS}Price[m,e] * x[m,e] <= 1000;

s.t. C2 {e in EVENTS} :
	sum{m in MARKETS}Payout[m,e] * x[m,e] >= minpayout;


