set DEST, := {1..6};

param TZERO, >= 0;

set CITIES, := {1..9};

param sqrt_offset, default .01;

param CCR, >= 0;

set ROADS dimen 2, within (CITIES cross CITIES);

set TRIPS dimen 2, within (DEST cross DEST);

param total_flow{(i,j) in ROADS};

param cmin{(i,j) in ROADS}, > 0;

param tr_matr{(k,l) in TRIPS};

param cost{(i,j) in ROADS}, >= 0;

param alpha{(i,j) in ROADS}, >= 0;


var capacity{(i,j) in ROADS}, >= cmin[i,j];


node Balance {(k,l) in TRIPS, j in CITIES} :
	net_in = if l = j then tr_matr[k,l] else if k = j then -tr_matr[k,l] else 0;

arc flow {(k,l) in TRIPS, (i,j) in ROADS} >= 0,
	 from Balance[k,l,i], to Balance[k,l,j];

minimize obj: sum{(i,j) in ROADS}(cost[i,j] * alpha[i,j] * sqrt(capacity[i,j] - cmin[i,j] + sqrt_offset) + total_flow[i,j] * cost[i,j] * (TZERO + CCR * (total_flow[i,j]/capacity[i,j]) ^ 2));


