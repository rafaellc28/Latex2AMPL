param B;

param N integer;

param A{j in 1..N};


var x{j in 1..N} binary;


maximize obj: sum{j in 1..N}A[j] * x[j];

s.t. C1  : sum{j in 1..N}A[j] * x[j], <= B;


solve;


data;

param B := 0;

param N := 0;

param A :=;


end;
