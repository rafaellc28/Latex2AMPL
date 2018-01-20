set ISO dimen 2;

set ADJACENT;

set REST;

set TYPE2 dimen 2;


var Assign2{(i1,i2) in ISO, j in REST} integer >= 0;


s.t. C1 {(i1,i2) in ISO, j in REST} :
	Assign2[i1,i2,j] = 0 or Assign2[i1,i2,j] + sum{ii1 in ADJACENT[i1] : (ii1,i2) in TYPE2}Assign2[ii1,i2,j] >= 2;


