set I;

param utc, := prod{i in 1..2}(gmtime() - 1000000000);

param N, >= 1, default 50;

param Mu{i in I};

param seed, := utc - 100000 * floor(utc / 100000);

param Sigma{i1 in I, i2 in I};

set T, := 1..N;

param z{i in I, t in T}, := Normal(0, 1);

param Chol{i in I, j in I : i >= j}, := if i = j then sqrt(Sigma[i,i] - (sum{k in I : k < i}(Chol[i,k] * Chol[i,k]))) else (Sigma[i,j] - sum{k in I : k < j}Chol[i,k] * Chol[j,k]) / Chol[j,j];

param x{i in I, t in T}, := Mu[i] + sum{j in I : i >= j}Chol[i,j] * z[j,t];

param xbar{i in I}, := (1 / card(T)) * sum{t in T}x[i,t];

param Cov{i in I, j in I}, := (1 / card(T)) * sum{t in T}(x[i,t] - xbar[i]) * (x[j,t] - xbar[j]);





solve;


data;

set I :=;

param N := 0;

param Mu :=;

param Sigma :=;


end;
