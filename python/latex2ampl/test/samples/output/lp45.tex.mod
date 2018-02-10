set COLOR;

set HOUSE;

set DRINK;

set PET;

set SMOKE;

set NATIONALITY;


var color{h in HOUSE, c in COLOR} binary;

var nationality{h in HOUSE, n in NATIONALITY} binary;

var drink{h in HOUSE, d in DRINK} binary;

var pet{h in HOUSE, p in PET} binary;

var smoke{h in HOUSE, s in SMOKE} binary;


s.t. C1 {h in HOUSE} :
	sum{c in COLOR}color[h,c] = 1;

s.t. C2 {c in COLOR} :
	sum{h in HOUSE}color[h,c] = 1;

s.t. C3 {h in HOUSE} :
	sum{n in NATIONALITY}nationality[h,n] = 1;

s.t. C4 {n in NATIONALITY} :
	sum{h in HOUSE}nationality[h,n] = 1;

s.t. C5 {h in HOUSE} :
	sum{d in DRINK}drink[h,d] = 1;

s.t. C6 {d in DRINK} :
	sum{h in HOUSE}drink[h,d] = 1;

s.t. C7 {h in HOUSE} :
	sum{s in SMOKE}smoke[h,s] = 1;

s.t. C8 {s in SMOKE} :
	sum{h in HOUSE}smoke[h,s] = 1;

s.t. C9 {h in HOUSE} :
	sum{p in PET}pet[h,p] = 1;

s.t. C10 {p in PET} :
	sum{h in HOUSE}pet[h,p] = 1;

s.t. C11 {h in HOUSE} :
	nationality[h,"Englishman"] = color[h,"red"];

s.t. C12 {h in HOUSE} :
	nationality[h,"Spaniard"] = pet[h,"dog"];

s.t. C13 {h in HOUSE} :
	drink[h,"coffee"] = color[h,"green"];

s.t. C14 {h in HOUSE} :
	nationality[h,"Ukranian"] = drink[h,"tea"];

s.t. C15 {h in HOUSE} :
	color[h,"green"] = if h = 1 then 0 else color[h - 1,"ivory"];

s.t. C16 {h in HOUSE} :
	smoke[h,"Old_Gold"] = pet[h,"snails"];

s.t. C17 {h in HOUSE} :
	smoke[h,"Kools"] = color[h,"yellow"];

s.t. C18 : drink[3,"milk"] = 1;

s.t. C19 : nationality[1,"Norwegian"] = 1;

s.t. C20 {h in HOUSE} :
	(1 - smoke[h,"Chesterfield"]) + (if h = 1 then 0 else pet[h - 1,"fox"]) + (if h = 5 then 0 else pet[h + 1,"fox"]) >= 1;

s.t. C21 {h in HOUSE} :
	(1 - smoke[h,"Kools"]) + (if h = 1 then 0 else pet[h - 1,"horse"]) + (if h = 5 then 0 else pet[h + 1,"horse"]) >= 1;

s.t. C22 {h in HOUSE} :
	smoke[h,"Lucky_Strike"] = drink[h,"orange_juice"];

s.t. C23 {h in HOUSE} :
	nationality[h,"Japanese"] = smoke[h,"Parliament"];

s.t. C24 {h in HOUSE} :
	(1 - nationality[h,"Norwegian"]) + (if h = 1 then 0 else color[h - 1,"blue"]) + (if h = 5 then 0 else color[h + 1,"blue"]) >= 1;


