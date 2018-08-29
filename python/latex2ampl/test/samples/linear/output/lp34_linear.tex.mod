set P;

set R;

param M, > 0;

param T, > 0;

param a{r in R, R}, >= 0;

param c{j in P, t in 1..T};

param b{r in R}, >= 0;

param d{i in R};

param f{i in R};


var x{p in P, t in 1..T}, >= 0;

var s{r in R, t1 in 1..T + 1}, >= 0;


maximize obj: sum{t in 1..T}(sum{j in P}c[j,t] * x[j,t] - sum{i in R}d[i] * s[i,t]) + sum{i in R}f[i] * s[i,T + 1];

s.t. C1 {t in 1..T} :
	sum{j in P}x[j,t] <= M;

s.t. C2 {i in R} :
	s[i,1] <= b[i];

s.t. C3 {i in R, t in 1..T} :
	s[i,t + 1] = s[i,t] - sum{j in P}a[i,j] * x[j,t];


