param entr;

param exit;

set ROADS dimen 2;

param cap{(i,j) in ROADS};


arc Traff {(i,j) in ROADS} >= 0, <= cap[i,j],
	 from {if i = entr} Entr_Int, from {if i != entr} Intersection[i], to {if j = exit} Exit_Int, to {if j != exit} Intersection[j], obj Entering_Traff (if i = entr then 1);


