set Sample;

param Sy{z in Sample};

param Sx{z in Sample};


var a;

var b;


s.t. C1  : sum{z in Sample}a * Sx[z] * Sx[z] + sum{z in Sample}b * Sx[z] = sum{z in Sample}Sy[z] * Sx[z];

s.t. C2  : sum{z in Sample}a * Sx[z] + sum{z in Sample}b = sum{z in Sample}Sy[z];


