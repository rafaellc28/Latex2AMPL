param ndim, := 10;

set rows1, := 1..(ndim + 1);

set rows, := 1..ndim;

set cols, := 1..ndim;

set cols1, := 1..(ndim + 1);

param givens{r in rows, c in cols} integer, >= 0, default 0;

set V dimen 2, := {(i,j) in {rows,cols} : givens[i,j] <> 0};

set B dimen 6, := {(i,j,k,l,m,n) in {V,rows,cols,rows1,cols1} : i >= k and i < m and j >= l and j < n and ((m - k) * (n - l)) = givens[i,j] and card({(s,t) in V : s >= k and s < m and t >= l and t < n}) = 1};


var x{(i,j,k,l,m,n) in B} binary;


minimize obj: 0;

s.t. C1 {(s,t) in {rows,cols}} :
	sum{(i,j,k,l,m,n) in B : s >= k and s < m and t >= l and t < n}x[i,j,k,l,m,n] = 1;


