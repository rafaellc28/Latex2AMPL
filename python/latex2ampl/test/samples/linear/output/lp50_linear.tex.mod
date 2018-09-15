set WIDTHS;

param roll_width;

param nPAT, >= 0;

param lambda, := 0.85;

set PATTERNS, := 1..nPAT;

param price{w in WIDTHS};

param orders{w in WIDTHS}, > 0;

param nbr{w in WIDTHS, p in PATTERNS} integer, >= 0;


var Use{w in WIDTHS} integer, >= 0;

var Cut{p in PATTERNS} integer, >= 0;


minimize obj: lambda * (sum{j in PATTERNS}Cut[j]) + (1 - lambda) * (1 - sum{i in WIDTHS}price[i] * Use[i]);

s.t. C1 {i in WIDTHS} :
	sum{j in PATTERNS}nbr[i,j] * Cut[j] >= orders[i];

s.t. C2 : sum{i in WIDTHS}i * Use[i] <= roll_width;


