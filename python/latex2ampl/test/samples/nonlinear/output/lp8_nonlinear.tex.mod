param a, >= 0;

param c, >= 0;

param b, >= 0;

param e, >= 0;

param d, >= 0;

param g, >= 0;

param f, >= 0;

param h, >= 0;

param N integer, := 8;

set I, := 1..N;


var x{i in I};


minimize obj: x[1] + x[2] + x[3];

s.t. C1  : 1 - a * (x[4] + x[6]) >= 0;

s.t. C2  : 1 - a * (x[5] + x[7] - x[4]) >= 0;

s.t. C3  : 1 - b * (x[8] - x[5]) >= 0;

s.t. C4  : x[1] * x[6] - c * x[4] - d * x[1] + e >= 0;

s.t. C5  : x[2] * x[7] - f * x[5] - x[2] * x[4] + f * x[4] >= 0;

s.t. C6  : x[3] * x[8] - g - x[3] * x[5] + h * x[5] >= 0;

s.t. C7  : 100 <= x[1] <= 10000;

s.t. C8 {i in {2,3}} :
	1000 <= x[i] <= 10000;

s.t. C9 {i in 4..8} :
	10 <= x[i] <= 1000;


