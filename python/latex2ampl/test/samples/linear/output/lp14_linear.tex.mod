param N integer, > 1;

param Lsup, := N / 2 - 1;

set I, := 1..Lsup;


var y{i in I}, := i / Lsup, <= 1, >= 0;

var x{i in I}, := .5, <= 1, >= 0;


s.t. C1 {i in ceil(Lsup / 2)..Lsup, j in max(1,Lsup - i)..min(Lsup + 1 - i,i)} :
	(x[i] + x[j]) ^ 2 + (y[i] - y[j]) ^ 2 = 1;

s.t. C2 : x[Lsup] ^ 2 + y[Lsup] ^ 2 = 1;

s.t. C3 {i in 2..Lsup} :
	y[i] >= y[i - 1];

maximize obj: sum{i in 2..Lsup - 1}y[i] * (x[i - 1] - x[i + 1]) + x[Lsup] + y[Lsup] * x[Lsup - 1] - x[2] * y[1];


