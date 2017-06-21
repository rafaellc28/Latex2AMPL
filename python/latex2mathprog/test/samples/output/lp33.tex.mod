param Rportfolio;

set S;

set T;

param Rt{s in S, t in T};

param R{s in S};


var y{t in T} >= 0;

var z{t in T} >= 0;

var w{s in S} >= 0;


minimize obj: (1 / card(T)) * sum{t in T}(y[t] + z[t]);

s.t. C1  : sum{s in S}w[s] * R[s], >= Rportfolio;

s.t. C2  : sum{s in S}w[s], = 1;

s.t. C3 {t in T} :
	(y[t] - z[t]), = sum{s in S}(Rt[s,t] - R[s]) * w[s];


solve;


data;

param Rportfolio := 0;

set S :=;

set T :=;

param Rt :=;

param R :=;


end;
