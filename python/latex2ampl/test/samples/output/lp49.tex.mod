set I;

param Y{i in I};

param X{i in I};


var a;

var b;

var u{i in I} >= 0;

var v{i in I} >= 0;


minimize obj: sum{i in I}u[i] + sum{i in I}v[i];

s.t. C1 {i in I} :
	b * X[i] + a + u[i] - v[i] = Y[i];


