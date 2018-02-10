param given{i in 1..9, j in 1..9} integer, in 0..9;


var X{i in 1..9, j in 1..9} integer, in 1..9;


s.t. C1 {i in 1..9, j in 1..9 : given[i,j] > 0} :
	X[i,j] = given[i,j];

s.t. C2 {i in 1..9} :
	alldiff{j in 1..9} X[i,j];

s.t. C3 {j in 1..9} :
	alldiff{i in 1..9} X[i,j];

s.t. C4 {I in 1..9 by 3, J in 1..9 by 3} :
	alldiff{i in I..I + 2, j in J..J + 2} X[i,j];


