param pi, := 4 * atan(1);


var x{1..2};


minimize obj: x[1] ^ 2 - 12 * x[1] + 11 + 10 * cos(pi * x[1] / 2) + 8 * sin(pi * 5 * x[1]) - exp(-(x[2] - .5) ^ 2 / 2) / sqrt(5);

s.t. C1 : -30 <= x[1] <= 30;

s.t. C2 : -10 <= x[2] <= 10;


