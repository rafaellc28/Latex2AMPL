set D_CITY;

param pd_cost{i in D_CITY};

param pd_cap{i in D_CITY};

param pd_loss{i in D_CITY};


arc PD_Ship {i in D_CITY} >= 0, <= pd_cap[i],
	 from Plant, to Dist[i] 1 - pd_loss[i], obj Total_Cost pd_cost[i];


