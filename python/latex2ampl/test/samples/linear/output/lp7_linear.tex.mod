set MAT;

set ACT;

param io{i in MAT, j in ACT};

param act_min{j in ACT}, >= 0;

param revenue{j in ACT};

param act_max{j in ACT}, >= act_min[j];


var Run{j in ACT}, <= act_max[j], >= act_min[j];


maximize obj: sum{j in ACT}revenue[j] * Run[j];

s.t. C1 {i in MAT} :
	sum{j in ACT}io[i,j] * Run[j] = 0;


