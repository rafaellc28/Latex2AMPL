param d integer, default 2, > 0;

param N integer, default 10, > 0;

set I, := {1..N};

set D, := 1..d;

set P dimen 2, := {i in I, j in 1..i - 1};


var x{i in I, k in D}, default i;

var r{(i,j) in P}, = sqrt(sum{k in D}(x[i,k] - x[j,k]) ^ 2);


minimize obj: sum{(i,j) in P}(r[i,j] ^ (-12) - 2 * r[i,j] ^ (-6));


