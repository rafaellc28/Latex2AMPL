param B;

param N integer;

param A{j in 1..N};


var x{j in 1..N} binary;


maximize obj: sum{j in 1..N}A[j] * x[j];

s.t. C1  : sum{j in 1..N}A[j] * x[j] <= B;


