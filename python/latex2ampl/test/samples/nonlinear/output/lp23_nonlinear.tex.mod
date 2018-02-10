var x{1..2};


minimize obj: -1;

s.t. C1 : x[1] * x[1] + x[2] * x[2] = 25;

s.t. C2 : x[1] * x[2] = 9;


