param avail, >= 0;

set PROD;

param profit{p in PROD};

param rate{p in PROD}, > 0;

param market{p in PROD}, >= 0;


var Make{p in PROD}, <= market[p], >= 0;


maximize obj: sum{p in PROD}profit[p] * Make[p];

s.t. C1 : sum{p in PROD}(1/rate[p]) * Make[p] <= avail;


