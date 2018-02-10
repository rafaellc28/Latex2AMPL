set Sample;

param Sy{z in Sample};

param Sx{z in Sample};


var Y;

var X;

var Ey{z in Sample};

var Ex{z in Sample};


s.t. C1 {z in Sample} :
	X + Ex[z] = Sx[z];

s.t. C2 : sum{z in Sample}Ex[z] = 0;

s.t. C3 {z in Sample} :
	Y + Ey[z] = Sy[z];

s.t. C4 : sum{z in Sample}Ey[z] = 0;


