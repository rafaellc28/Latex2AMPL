set I;

param y{i in I};

param x{i in I};


var u{i in I} >= 0;

var v{i in I} >= 0;

var a;

var b;


minimize obj: sum{i in I}u[i] + sum{i in I}v[i];

s.t. C1 {i in I} :
	b * x[i] + a + u[i] - v[i], = y[i];


solve;


data;

set I :=;

param y :=;

param x :=;


end;
