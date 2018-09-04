param p_supply, >= 0;

set D_CITY;

set W_CITY;

set DW_LINKS dimen 2, within (D_CITY cross W_CITY);

param dw_cap{(dl1,dl2) in DW_LINKS}, >= 0;

param pd_cost{dc in D_CITY}, >= 0;

param pd_cap{dc in D_CITY}, >= 0;

param dw_cost{(dl1,dl2) in DW_LINKS}, >= 0;

param w_demand{wc in W_CITY}, >= 0;


var PD_Ship{i in D_CITY}, <= pd_cap[i], >= 0;

var DW_Ship{(i,j) in DW_LINKS}, <= dw_cap[i,j], >= 0;


minimize obj: sum{i in D_CITY}pd_cost[i] * PD_Ship[i] + sum{(i,j) in DW_LINKS}dw_cost[i,j] * DW_Ship[i,j];

s.t. C1 : sum{i in D_CITY}PD_Ship[i] = p_supply;

s.t. C2 {i in D_CITY} :
	PD_Ship[i] = sum{(i,j) in DW_LINKS}DW_Ship[i,j];

s.t. C3 {j in W_CITY} :
	sum{(i,j) in DW_LINKS}DW_Ship[i,j] = w_demand[j];


