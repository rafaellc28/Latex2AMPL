set LETTERS, := {'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'};

set WORDS;

param total{word in WORDS};

set VALUES, := 1..card(LETTERS);


var x{i in LETTERS, j in VALUES} binary;


s.t. C1 {i in LETTERS} :
	sum{j in VALUES}x[i,j] = 1;

s.t. C2 {j in VALUES} :
	sum{i in LETTERS}x[i,j] = 1;

s.t. C3 {word in WORDS} :
	sum{k in 1..length(word), j in VALUES}j * x[substr(word,k,1),j] = total[word];


