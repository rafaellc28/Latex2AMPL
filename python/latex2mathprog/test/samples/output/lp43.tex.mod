set B dimen 6;

set rows;

set cols;


var x{(i,j,k,l,m,n) in B} binary;


minimize obj: 0;

s.t. C1 {(s,t) in {rows,cols}} :
	sum{(i,j,k,l,m,n) in B : s >= k and s < m and t >= l and t < n}x[i,j,k,l,m,n], = 1;


solve;


data;

set B :=;

set rows :=;

set cols :=;


end;
