param n integer, > 0;


var Row{i in 1..n} integer, <= n, >= 1;


s.t. C1 : alldiff{j in 1..n} Row[j];

s.t. C2 : alldiff{j in 1..n} Row[j] + j;

s.t. C3 : alldiff{j in 1..n} Row[j] - j;


