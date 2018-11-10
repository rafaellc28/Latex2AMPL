param p_supply, >= 0;

set D_CITY;

set W_CITY;

set DW_LINKS dimen 2, within (D_CITY cross W_CITY);

param dw_cap{(i,j) in DW_LINKS}, >= 0;

param pd_cost{dc in D_CITY}, >= 0;

param pd_cap{dc in D_CITY}, >= 0;

param dw_cost{(i,j) in DW_LINKS}, >= 0;

param w_demand{wc in W_CITY}, >= 0;


minimize Total_Cost;

node Plant : net_out = p_supply;

node Dist {i in D_CITY};

node Whse {j in W_CITY} :
	net_in = w_demand[j];

arc PD_Ship {i in D_CITY} >= 0, <= pd_cap[i],
	 from Plant, to Dist[i], obj Total_Cost pd_cost[i];

arc DW_Ship {(i,j) in DW_LINKS} >= 0, <= dw_cap[i,j],
	 from Dist[i], to Whse[j], obj Total_Cost dw_cost[i,j];


