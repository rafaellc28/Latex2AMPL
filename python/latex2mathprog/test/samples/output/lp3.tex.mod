var x1 integer >= 0;

var x2 integer >= 0;


maximize obj: 3 * x1 + 2 * x2;

s.t. C1  : 1.85 * x1 + x2, <= 100;

s.t. C2  : x1 + x2, <= 80;

s.t. C3  : x1, <= 40;


solve;


end;
