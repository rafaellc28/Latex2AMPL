param NumColors;

set Countries;

set Neighbors dimen 2, within Countries cross Countries;


var color{c in Countries} integer, <= NumColors, >= 1;


s.t. C1 {(c1,c2) in Neighbors} :
	color[c1] != color[c2];


