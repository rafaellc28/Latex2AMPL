param givens{i in 1..9, j in 1..9} integer, <= 9,>= 0, default 0;


var x{i in 1..9, j in 1..9, k in 1..9} binary;


s.t. C1 {i in 1..9, j in 1..9, k in 1..9 : givens[i,j] <> 0} :
	x[i,j,k], = if givens[i,j] = k then 1 else 0;

s.t. C2 {i1 in 1..9 by 3, j1 in 1..9 by 3, k in 1..9} :
	sum{i in i1..i1 + 2, j in j1..j1 + 2}x[i,j,k], = 1;

s.t. C3 {i in 1..9, j in 1..9} :
	sum{k in 1..9}x[i,j,k], = 1;

s.t. C4 {i in 1..9, k in 1..9} :
	sum{j in 1..9}x[i,j,k], = 1;

s.t. C5 {j in 1..9, k in 1..9} :
	sum{i in 1..9}x[i,j,k], = 1;


solve;


data;

param givens :=;


end;
