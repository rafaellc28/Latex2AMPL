param Q;

param P;

param T;

set X;

param N;

set U{x in X};


var V{t in 0..T, x in X} >= 0;


minimize obj: sum{t in 0..T - 1, x in X}V[t,x];

s.t. C1 {t in 0..T - 1, x in 1..N, u in U[x]} :
	V[t,x], >= P * V[t + 1,x + u] + Q * V[t + 1,x - u];

s.t. C2 {x in X} :
	V[T,x], = log(x);

s.t. C3 {t in 0..T, x in X} :
	V[t,x], >= 0;

s.t. C4 {x in X, u in U[x]} :
	u, >= 0;


solve;


data;

param Q := 0;

param P := 0;

param T := 0;

set X :=;

param N := 0;

set U[0] :=;


end;
