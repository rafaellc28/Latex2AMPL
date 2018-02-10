param numTanks integer, > 0;

param numJobs integer, > 0;

param minTime{i in 1..numTanks};

param maxTime{i in 1..numTanks};

param full{i in 0..numTanks};

param empty{i in 0..numTanks, 0..numTanks};

param perMax, = sum{i in 1..numTanks}maxTime[i];


var Entry{i in 0..numTanks} integer, <= numJobs * perMax, >= 0;

var Period integer, <= perMax, >= 0;

var Removal{i in 0..numTanks} integer, <= numJobs * perMax, >= 0;


minimize obj: Period;

s.t. C1 {t in 0..numTanks} :
	Removal[t] + full[t] = Entry[(t + 1) mod (numTanks + 1)];

s.t. C2 {t in 1..numTanks} :
	Entry[t] + minTime[t] <= Removal[t] and Entry[t] + maxTime[t] >= Removal[t];

s.t. C3 {t1 in 0..numTanks - 1, t2 in t1 + 1..numTanks, k in 1..numJobs - 1} :
	Entry[(t1 + 1) mod (numTanks + 1)] + empty[(t1 + 1) mod (numTanks + 1),t2] <= Removal[t2] - k * Period or Entry[(t2 + 1) mod (numTanks + 1)] + empty[(t2 + 1) mod (numTanks + 1),t1] <= Removal[t1] + k * Period;

s.t. C4 : Removal[0] = 0;

s.t. C5 : Removal[numTanks] + full[numTanks] <= numJobs * Period;


