set ROADS dimen 2;

param entr;

param cap{(i,j) in ROADS};


arc Traff {(i,j) in ROADS} >= 0, <= cap[i,j],
	 from Intersection[i], to Intersection[j], obj Entering_Traff (if i = entr then 1);


