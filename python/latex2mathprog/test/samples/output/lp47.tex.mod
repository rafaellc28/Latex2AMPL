set I;

param BigM;

param A{i in I};


var y{i in I, j in I} binary;

var t{i in I};


s.t. C1 {i in I, j in I : i <> j} :
	A[i], <= A[j] + BigM * y[i,j];

s.t. C2 {i in I, j in I : i <> j} :
	A[j], <= A[i] + BigM * (1 - y[i,j]);

s.t. C3 {i in I, j in I : i <> j} :
	y[i,j] + y[j,i], = 1;

s.t. C4 {i in I} :
	t[i], = 1 + sum{j in I : i <> j}y[i,j];


solve;


data;

set I :=;

param BigM := 0;

param A :=;


end;
