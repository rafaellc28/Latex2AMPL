param a, := .99;

param b, := .9;

param n, := 10;

set I, := 1..n;

param x0{i in I};

param lb{i in I};

param ub{i in I}, > lb[i];


var x{i in I}, := x0[i], <= ub[i], >= lb[i];

var G5, = 1.12 * x[1] + .13167 * x[1] * x[8] - .00667 * x[1] * x[8] ^ 2 - a * x[4];

var G2, = -133 + 3 * x[7] - a * x[10];

var G1, = 35.82 - .222 * x[10] - b * x[9];

var G6, = 57.425 + 1.098 * x[8] - .038 * x[8] ^ 2 + .325 * x[6] - a * x[7];


minimize obj: 5.04 * x[1] + .035 * x[2] + 10 * x[3] + 3.36 * x[5] - .063 * x[4] * x[7];

s.t. C1 : G1 >= 0;

s.t. C2 : G2 >= 0;

s.t. C3 : -G1 + x[9] * (1 / b - b) >= 0;

s.t. C4 : -G2 + (1 / a - a) * x[10] >= 0;

s.t. C5 : G5 >= 0;

s.t. C6 : G6 >= 0;

s.t. C7 : -G5 + (1 / a - a) * x[4] >= 0;

s.t. C8 : -G6 + (1 / a - a) * x[7] >= 0;

s.t. C9 : 1.22 * x[4] - x[1] - x[5] = 0;

s.t. C10 : 98000 * x[3] / (x[4] * x[9] + 1000 * x[3]) - x[6] = 0;

s.t. C11 : (x[2] + x[5]) / x[1] - x[8] = 0;


