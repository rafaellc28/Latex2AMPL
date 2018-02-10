param utc, := prod{i in 1..2}(gmtime() - 1000000000);

set S;

param N, default 5000;

param r{i in S};

param seed, := utc - 100000 * floor(utc / 100000);

set T, := 1..N;

param cov{s1 in S, s2 in S};

param rportfolio, default (1 / card(S)) * sum{i in S}r[i];

param zn{j in S, t in T}, := Normal(0, 1);

param c{i in S, j in S : i >= j}, := if i = j then sqrt(cov[i,i] - (sum{k in S : k < i}(c[i,k] * c[i,k]))) else (cov[i,j] - sum{k in S : k < j}c[i,k] * c[j,k]) / c[j,j];

param rt{i in S, t in T}, := r[i] + sum{j in S : j <= i}c[i,j] * zn[j,t];


var y{t in T} >= 0;

var z{t in T} >= 0;

var w{s in S} >= 0;


minimize obj: (1 / card(T)) * sum{t in T}(y[t] + z[t]);

s.t. C1 : sum{s in S}w[s] * r[s] >= rportfolio;

s.t. C2 : sum{s in S}w[s] = 1;

s.t. C3 {t in T} :
	(y[t] - z[t]) = sum{s in S}(rt[s,t] - r[s]) * w[s];


