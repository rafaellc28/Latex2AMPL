var x{1..2}, := 2;


minimize obj: 0.01 * x[1] ^ 2 + x[2] ^ 2;

s.t. C1  : x[1] * x[2] - 25 >= 0;

s.t. C2  : x[1] ^ 2 + x[2] ^ 2 - 25 >= 0;

s.t. C3  : x[1] >= 2;

