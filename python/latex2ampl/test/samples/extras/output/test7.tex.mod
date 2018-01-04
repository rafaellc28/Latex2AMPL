var x{1..3, 1..6} integer >= 0;


maximize obj: 3 * x[1,1] + 2 * x[2,2];

s.t. C1  : x[1,3] + x[1,6] <= 80;

s.t. C2  : x[3,2] + x[3,2] <= 100;


