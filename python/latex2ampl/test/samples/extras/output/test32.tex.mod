param giveLoc;

set PEOPLE;

param hiTargetLoc;

set REST;

set ISO dimen 2;

set ADJACENT;

param hiTargetTitle;

param giveTitle;

set TYPE2 dimen 2;

param number2{(i1,i2) in ISO};

param hiDine{j in REST};

param give{(i1,i2) in ISO};

param upperbnd{(i1,i2) in ISO, j in REST}, := min(ceil((number2[i1,i2]/(card(PEOPLE))) * hiDine[j]) + give[i1,i2],hiTargetTitle[i1,j] + giveTitle[i1],hiTargetLoc[i2,j] + giveLoc[i2],number2[i1,i2]);


var Lone{(i1,i2) in ISO, j in REST} binary;

var Assign2{(i1,i2) in ISO, j in REST} integer >= 0;


s.t. C1 {(i1,i2) in ISO, j in REST} :
	Assign2[i1,i2,j] <= upperbnd[i1,i2,j] * Lone[i1,i2,j];

s.t. C2 {(i1,i2) in ISO, j in REST} :
	Assign2[i1,i2,j] + sum{ii1 in ADJACENT[i1] : (ii1,i2) in TYPE2}Assign2[ii1,i2,j] >= 2 * Lone[i1,i2,j];

s.t. C3 {(i1,i2) in ISO, j in REST} :
	Assign2[i1,i2,j] >= Lone[i1,i2,j];


