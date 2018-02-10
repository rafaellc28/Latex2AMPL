set C;


var x{1..2, 1..2, c in C} integer >= 0;


maximize obj {c in C}: 3 * x[1,1,c] + 2 * x[2,2,c];

s.t. C1 : 1.85 * x[1] + x[2] <= 100;

s.t. C2 : x[1] + x[2] <= 80;

s.t. C3 : x[1] <= 40;


