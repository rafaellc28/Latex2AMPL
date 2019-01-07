set nodes;

param orig symbolic, in nodes;

param dest symbolic, in nodes, != orig;

set arcs dimen 2, within (nodes diff {dest}) cross (nodes diff {orig});

param cap{(i,j) in arcs}, >= 0;


var Flow{(i,j) in arcs}, <= cap[i,j], >= 0;


maximize obj: sum{(orig,j) in arcs}Flow[orig,j];

s.t. C1 {k in nodes diff {orig,dest}} :
	sum{(i,k) in arcs}Flow[i,k] = sum{(k,j) in arcs}Flow[k,j];


