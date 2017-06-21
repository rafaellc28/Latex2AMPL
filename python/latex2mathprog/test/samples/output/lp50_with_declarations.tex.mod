set I;

param y{i in I};

param x{i in I};


var z;

var a;

var b;

var u{i in I} >= 0;

var v{i in I} >= 0;


minimize obj: z;

s.t. C1 {i in I} :
	b * x[i] + a + u[i] - v[i], = y[i];

s.t. C2 {i in I} :
	z - u[i], >= 0;

s.t. C3 {i in I} :
	z - v[i], >= 0;


solve;


data;

set I :=;

param y :=;

param x :=;


end;
