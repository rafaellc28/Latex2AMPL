set I;

param D{j in 1..10};


s.t. C1 {i in I : 1 = 1 or alldiff{j in 1..10} D[j]} :
	1 < 2;


