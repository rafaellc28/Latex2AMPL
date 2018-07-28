param p, := 0.55, <= 1, >= 0;

param T, := 5, >= 1;

param N, := 50, >= 1;

param q, := 1 - p, <= 1 - p, >= 0;

set X, := 1..N;

param B, := N, <= N, >= 1;

set U{x in X}, := 0..min(B,min(N - x,x - 1));


var V{t in 0..T, x in X} >= 0;


minimize obj: sum{t in 0..T - 1, x in X}V[t,x];

s.t. C1 {t in 0..T - 1, x in 1..N, u in U[x]} :
	V[t,x] >= p * V[t + 1,x + u] + q * V[t + 1,x - u];

s.t. C2 {x in X} :
	V[T,x] = log(x);


