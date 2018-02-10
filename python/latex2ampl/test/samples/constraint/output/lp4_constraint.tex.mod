param n;

set ROWS, := {1..n};

set COLUMNS, := {1..n};


var X{r in ROWS, c in COLUMNS} binary;


s.t. C1 {j in COLUMNS} :
	sum{i in ROWS}X[i,j] = 1;

s.t. C2 {i in ROWS} :
	sum{j in COLUMNS}X[i,j] = 1;

s.t. C3 {k in 2..2 * n} :
	sum{i in ROWS, j in COLUMNS : i + j = k}X[i,j] <= 1;

s.t. C4 {k in -(n - 1)..(n - 1)} :
	sum{i in ROWS, j in COLUMNS : i - j = k}X[i,j] <= 1;


