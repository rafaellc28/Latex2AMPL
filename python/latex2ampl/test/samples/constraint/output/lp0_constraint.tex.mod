param sample integer, > 0;

set CATEG;

param numberGrps integer, > 0;

set ALL_PEOPLE ordered;

param selection integer, < sample, >= 0;

param type{i in ALL_PEOPLE, k in CATEG} symbolic;

param typeWt{k in CATEG}, >= 0;

set PEOPLE, := {i in ALL_PEOPLE : ord(i) mod sample = selection};

set TYPES{k in CATEG}, := setof {i in PEOPLE} type[i,k];


var MaxInGrp, >= ceil(card(PEOPLE)/numberGrps);

var MinInGrp, <= floor(card(PEOPLE)/numberGrps);

var MinType{k in CATEG, t in TYPES[k]}, <= floor(card({i in PEOPLE : type[i,k] = t})/numberGrps);

var Assign{i in PEOPLE, j in 1..numberGrps} binary;

var MaxType{k in CATEG, t in TYPES[k]}, >= ceil(card({i in PEOPLE : type[i,k] = t})/numberGrps);


minimize obj: (MaxInGrp - MinInGrp) + sum{k in CATEG, t in TYPES[k]}typeWt[k] * (MaxType[k,t] - MinType[k,t]);

s.t. C1 {i in PEOPLE} :
	sum{j in 1..numberGrps}Assign[i,j] = 1;

s.t. C2 {j in 1..numberGrps} :
	MinInGrp <= sum{i in PEOPLE}Assign[i,j];

s.t. C3 {j in 1..numberGrps} :
	MaxInGrp >= sum{i in PEOPLE}Assign[i,j];

s.t. C4 {j in 1..numberGrps, k in CATEG, t in TYPES[k]} :
	MinType[k,t] <= sum{i in PEOPLE : type[i,k] = t}Assign[i,j];

s.t. C5 {j in 1..numberGrps, k in CATEG, t in TYPES[k]} :
	MaxType[k,t] >= sum{i in PEOPLE : type[i,k] = t}Assign[i,j];


