var x{1..3} >= 0;


minimize obj: 9 - 8 * x[1] - 6 * x[2] - 4 * x[3] + 2 * x[1] * x[1] + 2 * x[2] * x[2] + x[3] * x[3] + 2 * x[1] * x[2] + 2 * x[1] * x[3];

s.t. C1  : 3 >= x[1] + x[2] + 2 * x[3];

