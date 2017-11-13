set Sample;

param Sy{z in Sample};

param Sx{z in Sample};


var q;

var p;

var b;

var a;


s.t. C1  : sum{z in Sample}q * Sy[z] * Sy[z] + sum{z in Sample}p * Sy[z] = sum{z in Sample}Sy[z] * Sx[z];

s.t. C2  : sum{z in Sample}q * Sy[z] + sum{z in Sample}p = sum{z in Sample}Sx[z];

s.t. C3  : sum{z in Sample}a * Sx[z] * Sx[z] + sum{z in Sample}b * Sx[z] = sum{z in Sample}Sy[z] * Sx[z];

s.t. C4  : sum{z in Sample}a * Sx[z] + sum{z in Sample}b = sum{z in Sample}Sy[z];


