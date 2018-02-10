param sample integer, > 0;

set CATEG;

param numberGrps integer, > 0;

set ALL_PEOPLE ordered;

param selection integer, < sample, >= 0;

param type{i in ALL_PEOPLE, k in CATEG} symbolic;

param typeWt{k in CATEG}, >= 0;

set PEOPLE, := {i in ALL_PEOPLE : ord(i) mod sample = selection};

set TYPES{k in CATEG}, := setof {i in PEOPLE} type[i,k];


var MaxInGrp integer, >= ceil(card(PEOPLE)/numberGrps);

var MinInGrp integer, <= floor(card(PEOPLE)/numberGrps);

var MinType{k in CATEG, t in TYPES[k]} integer, <= floor(card({i in PEOPLE : type[i,k] = t})/numberGrps);

var Assign{i in PEOPLE} integer >= 1, <= numberGrps;

var MaxType{k in CATEG, t in TYPES[k]} integer, >= ceil(card({i in PEOPLE : type[i,k] = t})/numberGrps);


minimize obj: (MaxInGrp - MinInGrp) + sum{k in CATEG, t in TYPES[k]}typeWt[k] * (MaxType[k,t] - MinType[k,t]);

s.t. C1 {j in 1..numberGrps} :
	MinInGrp <= numberof j in ({i in PEOPLE} Assign[i]);

s.t. C2 {j in 1..numberGrps} :
	MaxInGrp >= numberof j in ({i in PEOPLE} Assign[i]);

s.t. C3 {j in 1..numberGrps, k in CATEG, t in TYPES[k]} :
	MinType[k,t] <= numberof j in ({i in PEOPLE : type[i,k] = t} Assign[i]);

s.t. C4 {j in 1..numberGrps, k in CATEG, t in TYPES[k]} :
	MaxType[k,t] >= numberof j in ({i in PEOPLE : type[i,k] = t} Assign[i]);


