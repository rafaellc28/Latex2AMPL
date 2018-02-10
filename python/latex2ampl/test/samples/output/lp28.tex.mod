param A;

param Q;

set X;

param P;

param N;

set U{x in X};


var V{x in X};


minimize obj: sum{x in X}V[x];

s.t. C1 {x in 1..N - 1, u in U[x]} :
	V[x] >= A * (P * V[x + u] + Q * V[x - u]);

s.t. C2 : V[0] = 0;

s.t. C3 : V[N] = N;

s.t. C4 {x in X} :
	V[x] >= 0;

s.t. C5 {x in X, u in U[x]} :
	u >= 0;


