param nPeople integer, > 0;

set PREFS dimen 2, within {i1 in 1..nPeople, i2 in 1..nPeople : i1 != i2};


var Pos{i in 1..nPeople} integer, <= nPeople, >= 1;

var Sat{(i1,i2) in PREFS} binary;


maximize obj: sum{(i1,i2) in PREFS}Sat[i1,i2];

s.t. C1 : alldiff{i in 1..nPeople} Pos[i];

s.t. C2 {(i1,i2) in PREFS} :
	Sat[i1,i2] = 1 <==> Pos[i1] - Pos[i2] = 1 or Pos[i2] - Pos[i1] = 1;

s.t. C3 : Pos[1] < Pos[2];


