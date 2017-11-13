set S;

param numhrs;

set D;

set H, := 1..numhrs;

param shifts{d in D, h in H, s in S};

param dmnd{h in H, d in D};


var crew{s in S} integer >= 0;


minimize obj: sum{s in S}crew[s];

s.t. C1 {h in H, d in D} :
	sum{s in S}crew[s] * shifts[d,h,s] >= dmnd[h,d];


