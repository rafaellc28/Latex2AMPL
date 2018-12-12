set MAT;

set ACT;

param io{i in MAT, j in ACT};

param act_min{j in ACT}, >= 0;

param revenue{j in ACT};

param act_max{j in ACT}, >= act_min[j];


maximize Net_Profit;

s.t. Balance {i in MAT} :
	to_come = 0;

var Run{j in ACT}, <= act_max[j], >= act_min[j], coeff {i in MAT} Balance[i] io[i,j], obj Net_Profit revenue[j];


