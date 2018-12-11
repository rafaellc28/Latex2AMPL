set SHIFTS;

param Nsched;

set SCHEDS, := 1..Nsched;

param rate{s in SCHEDS}, >= 0;

param required{s in SCHEDS}, >= 0;

set SHIFT_LIST{s in SCHEDS}, within SHIFTS;


minimize Total_Cost;

s.t. Shift_Needs {i in SHIFTS} :
	to_come >= required[i];

var Work{j in SCHEDS} >= 0, coeff {i in SHIFT_LIST[j]} Shift_Needs[i] 1, obj Total_Cost rate[j];


