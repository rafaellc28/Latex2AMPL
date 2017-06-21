set I;

param a{i in I};

param s{i in I}, := 1 + sum{j in I : a[i] < a[j] or a[i] = a[j] and i < j}1;

param r{i in I}, := 1 + sum{j in I}if (a[j] < a[i] or a[j] = a[i] and j < i) then 1 else 0;

param BigM, := 1 + sum{i in I}abs(a[i]);


var y{i in I, j in I : i <> j} binary;

var t{i in I};


s.t. C1 {i in I, j in I : i <> j} :
	a[i], <= a[j] + BigM * y[i,j];

s.t. C2 {i in I, j in I : i <> j} :
	a[j], <= a[i] + BigM * (1 - y[i,j]);

s.t. C3 {i in I, j in I : i <> j} :
	y[i,j] + y[j,i], = 1;

s.t. C4 {i in I} :
	t[i], = 1 + sum{j in I : i <> j}y[i,j];


solve;


data;

set I :=;

param a :=;


end;
