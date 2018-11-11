set INTER;

param entr symbolic, in INTER;

param exit symbolic, in INTER, != entr;

set ROADS dimen 2, within (INTER diff {exit}) cross (INTER diff {entr});

param cap{(i,j) in ROADS}, >= 0;


node Intersection {k in INTER};

arc Traff_In >= 0,
	 to Intersection[entr];

arc Traff_Out >= 0,
	 from Intersection[exit];

arc Traff {(i,j) in ROADS} >= 0, <= cap[i,j],
	 from Intersection[i], to Intersection[j];

maximize obj: Traff_In;


