set SCHEDS;

set SHIFTS;

param rate{j in SCHEDS};

param required{i in SHIFTS};

set SHIFT_LIST{j in SCHEDS};


minimize Total_Cost;

s.t. Shift_Needs {i in SHIFTS} :
	to_come >= required[i];

var Work{j in SCHEDS} >= 0, coeff {i in SHIFT_LIST[j]} Shift_Needs[i] 1, obj Total_Cost rate[j];


