set INTER;

param entr;

param exit;


node Intersection {k in INTER} :
	(if k = exit then -Infinity) <= net_out <= (if k = entr then Infinity);


