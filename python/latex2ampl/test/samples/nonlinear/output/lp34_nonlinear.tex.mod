set I, := 1..5;

set J, := 1..4;

param a{i in I, j in J};

param c{i in I};


var x{j in J} , <= 10, >= 0, := j;


minimize obj: -sum{i in I}1 / (sum{j in J}(x[j] - a[i,j]) ^ 2 + c[i]);


