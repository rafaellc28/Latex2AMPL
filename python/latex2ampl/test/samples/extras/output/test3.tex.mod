param M;


var x{i in M..10} integer >= 0;


maximize obj: 3 * x[1] + 2 * x[10];

s.t. C1 {i in 2..5} :
	x[i] + x[i + 1] <= 80;

s.t. C2 {i in M..9} :
	x[i] + x[i + 1] <= 100;


