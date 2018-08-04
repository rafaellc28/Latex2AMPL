param pi, := 4 * atan(1);

param N integer, > 0;

set I, := 1..N;


var the{i in I}, := pi * i / N, >= 0;

var rho{i in I}, := 4 * i * (N + 1 - i) / (N + 1) ^ 2, <= 1, >= 0;


s.t. C1 {i in I, j in i + 1..N} :
	rho[i] ^ 2 + rho[j] ^ 2 - 2 * rho[i] * rho[j] * cos(the[j] - the[i]) <= 1;

s.t. C2 {i in 2..N} :
	the[i] >= the[i - 1];

s.t. C3 : the[N] = pi;

s.t. C4 : rho[N] = 0;

maximize obj: .5 * sum{i in 2..N}rho[i] * rho[i - 1] * sin(the[i] - the[i - 1]);


