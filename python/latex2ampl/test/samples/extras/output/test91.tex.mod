param ppc;

set DW_LINKS dimen 2;

param dw_cap{(i,j) in DW_LINKS};

param dw_cost{(i,j) in DW_LINKS};


arc DW_Ship {(i,j) in DW_LINKS} >= 0, <= dw_cap[i,j],
	 from Dist[i], to Whse[j] (1000 / ppc), obj Total_Cost dw_cost[i,j];


