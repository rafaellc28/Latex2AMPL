param avail;

set PROD;

param rate{p in PROD};

param Make{p in PROD};


s.t. C1 : ((avail >= 0 or avail >= 2)) ==> sum{p in PROD}(1/rate[p]) * Make[p] <= avail;


