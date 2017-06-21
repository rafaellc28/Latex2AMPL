set I;

param Y{i in I};

param X{i in I};


var u{i in I} >= 0;

var v{i in I} >= 0;

var a;

var b;


minimize obj: sum{i in I}u[i] + sum{i in I}v[i];

s.t. C1 {i in I} :
	b * X[i] + a + u[i] - v[i], = Y[i];


solve;


data;

set I :=;

param Y :=;

param X :=;


end;
