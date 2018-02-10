var x{1..2};


minimize obj: (1 - x[1]) ^ 2;

s.t. C1 : 10 * (x[2] - x[1] ^ 2) = 0;


