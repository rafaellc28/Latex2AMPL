param avail;

set PROD;

param rate{p in PROD};

param market{p in PROD};


var Make{p in PROD} >= 0, <= market[p];


s.t. C1 {if avail > 0} :
	sum{p in PROD}(1/rate[p]) * Make[p] <= avail;


