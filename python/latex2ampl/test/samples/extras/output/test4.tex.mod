set C;


var x{1..3, 2..4, c in C} integer >= 0;


maximize obj {c in C}: 3 * x[1,2,c] + 2 * x[2,2,c];

s.t. C1 : x[1,3,5] + x[1,4,6] <= 80;

s.t. C2 : x[3,2,4] + x[3,2,5] <= 100;


