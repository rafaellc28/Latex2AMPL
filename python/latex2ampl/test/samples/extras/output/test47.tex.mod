set I;

param D{j in 1..10};


s.t. C1 {i in I : (((forall{j in 1..10} D[j] > 0)))} :
	1 < 2;


