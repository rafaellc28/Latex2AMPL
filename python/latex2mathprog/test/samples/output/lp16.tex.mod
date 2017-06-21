set TABLES;

set PAIRS dimen 2;

param TABLESIZE;

set PEOPLE;


var y{(p,q) in PAIRS} binary;

var x{p in PEOPLE, t in TABLES} binary;


maximize obj: sum{(p,q) in PAIRS}y[p,q];

s.t. C1 {p in PEOPLE} :
	sum{t in TABLES}x[p,t], = 1;

s.t. C2 {p in PEOPLE} :
	(sum{q in 1..(p - 1)}y[q,p]) + (sum{q in (p + 1)..card(PEOPLE)}y[p,q]), = TABLESIZE - 1;

s.t. C3 {t in TABLES, (p,q) in PAIRS} :
	y[p,q], >= x[p,t] + x[q,t] - 1;

s.t. C4 {t in TABLES} :
	sum{p in PEOPLE}x[p,t], = 3;


solve;


data;

set TABLES :=;

set PAIRS :=;

param TABLESIZE := 0;

set PEOPLE :=;


end;
