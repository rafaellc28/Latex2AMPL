set H;

set S;

set D;

param Shifts{d in D, h in H, s in S};

param Dmnd{h in H, d in D};


var crew{s in S} integer >= 0;


minimize obj: sum{s in S}crew[s];

s.t. C1 {h in H, d in D} :
	sum{s in S}crew[s] * Shifts[d,h,s], >= Dmnd[h,d];


solve;


data;

set H :=;

set S :=;

set D :=;

param Shifts :=;

param Dmnd :=;


end;
