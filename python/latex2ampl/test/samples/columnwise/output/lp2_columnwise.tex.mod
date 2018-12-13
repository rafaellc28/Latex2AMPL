set MAT;

set ACT;

set MATF, within MAT;

param cost{j in ACT}, >= 0;

param io{i in MAT, j in ACT};

param act_min{j in ACT}, >= 0;

param act_max{j in ACT}, >= act_min[j];

param sell_min{i in MATF}, >= 0;

param revenue{i in MATF}, >= 0;

param sell_max{i in MATF}, >= sell_min[i];


maximize Net_Profit;

s.t. Balance {i in MAT} :
	to_come = 0;

var Sell{i in MATF}, <= sell_max[i], >= sell_min[i], coeff Balance[i] -1, obj Net_Profit revenue[i];

var Run{j in ACT}, <= act_max[j], >= act_min[j], coeff {i in MAT} Balance[i] io[i,j], obj Net_Profit -cost[j];


