param a, := 1, <= 1, >= 0;

param p, := 0.25, <= 1, >= 0;

param N, := 100, >= 1;

param q, := 1 - p, <= 1 - p, >= 0;

set X, := 0..N;

param B, := N, <= N, >= 1;

set U{x in X}, := 1..min(B,min(N - x,x));


var V{x in X};


minimize obj: sum{x in X}V[x];

s.t. C1 {x in 1..N - 1, u in U[x]} :
	V[x] >= a * (p * V[x + u] + q * V[x - u]);

s.t. C2 : V[0] = 0;

s.t. C3 : V[N] = N;


