set VALUES;

set LETTERS;

set WORDS;

param Total{word in WORDS};


var x{i in LETTERS, j in VALUES} binary;


s.t. C1 {i in LETTERS} :
	sum{j in VALUES}x[i,j] = 1;

s.t. C2 {j in VALUES} :
	sum{i in LETTERS}x[i,j] = 1;

s.t. C3 {word in WORDS} :
	sum{k in 1..length(word), j in VALUES}j * x[substr(word,k,1),j] = Total[word];


