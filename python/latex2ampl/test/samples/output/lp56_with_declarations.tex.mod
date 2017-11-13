set oils;

param M, >= 0;

set month;

param productprice, >= 0;

param storagecost;

param buyingprices{m in month, o in oils};

param oilhardness{o in oils}, >= 0;


var buys{m1 in month, o in oils} >= 0;

var production{m in month} >= 0;

var useoilb{m in month, o in oils} binary;

var useoil{m in month, o in oils} >= 0;

var stock{m1 in month, o in oils} >= 0;


maximize obj: sum{m in month}productprice * production[m] - sum{m in month, o in oils}buyingprices[m,o] * buys[m,o] - sum{m in month, o in oils}storagecost * stock[m,o];

s.t. C1 {o in oils} :
	stock[1,o] = 500;

s.t. C2 {o in oils} :
	stock[6,o] + buys[6,o] - useoil[6,o] >= 500;

s.t. C3 {m in month, o in oils} :
	stock[m,o] <= 1000;

s.t. C4 {m in month, o in oils} :
	useoil[m,o] <= stock[m,o] + buys[m,o];

s.t. C5 {m1 in month, m2 in month, o in oils : m2 = m1 + 1} :
	stock[m2,o] = stock[m1,o] + buys[m1,o] - useoil[m1,o];

s.t. C6 {m in month} :
	sum{o in oils}oilhardness[o] * useoil[m,o] >= 3 * production[m];

s.t. C7 {m in month} :
	sum{o in oils}oilhardness[o] * useoil[m,o] <= 6 * production[m];

s.t. C8 {m in month} :
	production[m] = sum{o in oils}useoil[m,o];

s.t. C9 {m in month} :
	useoil[m,"VEG1"] + useoil[m,"VEG2"] <= 200;

s.t. C10 {m in month} :
	useoil[m,"OIL1"] + useoil[m,"OIL2"] + useoil[m,"OIL3"] <= 250;

s.t. C11 {m in month, o in oils} :
	M * useoilb[m,o] >= useoil[m,o];

s.t. C12 {m in month} :
	sum{o in oils}useoilb[m,o] <= 3;

s.t. C13 {m in month, o in oils} :
	20 * useoilb[m,o] <= useoil[m,o];

s.t. C14 {m in month} :
	useoilb[m,"VEG1"] <= useoilb[m,"OIL3"];

s.t. C15 {m in month} :
	useoilb[m,"VEG2"] <= useoilb[m,"OIL3"];


