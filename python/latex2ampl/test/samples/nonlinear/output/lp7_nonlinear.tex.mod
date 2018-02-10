set I, := 1..235;

param PI, := 4 * atan(1);

param y{i in I};


var x{i in 1..8};

var a{i in I}, = x[1] / x[6] * exp(-(y[i] - x[3]) ^ 2 / (2 * x[6] ^ 2));

var c{i in I}, = (1 - x[2] - x[1]) / x[8] * exp(-(y[i] - x[5]) ^ 2 / (2 * x[8] ^ 2));

var b{i in I}, = x[2] / x[7] * exp(-(y[i] - x[4]) ^ 2 / (2 * x[7] ^ 2));


minimize obj: -sum{i in I}log((a[i] + b[i] + c[i]) / sqrt(2 * PI));

s.t. C1 : 1 - x[1] - x[2] >= 0;

s.t. C2 {i in 1..2} :
	.001 <= x[i] <= .499;

s.t. C3 : 100 <= x[3] <= 180;

s.t. C4 : 130 <= x[4] <= 210;

s.t. C5 : 170 <= x[5] <= 240;

s.t. C6 {i in 6..8} :
	5 <= x[i] <= 25;


