set Sample;

param Sy{z in Sample};

param Sx{z in Sample};


var X;

var Y;

var Ex{z in Sample};

var Ey{z in Sample};


s.t. C1 {z in Sample} :
	X + Ex[z], = Sx[z];

s.t. C2  : sum{z in Sample}Ex[z], = 0;

s.t. C3 {z in Sample} :
	Y + Ey[z], = Sy[z];

s.t. C4  : sum{z in Sample}Ey[z], = 0;


solve;


data;

set Sample :=;

param Sy :=;

param Sx :=;


end;
