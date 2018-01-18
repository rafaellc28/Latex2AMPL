param c, > 0;

param m integer, > 0;

set I, := 1..m;

param w{i in 1..m}, > 0;

param z{i in I, j in 1..m}, := if i = 1 and j = 1 then 1 else if exists{jj in 1..j - 1} z[i,jj] then 0 else if sum{ii in 1..i - 1}w[ii] * z[ii,j] + w[i] > c then 0 else 1;

param n, := sum{j in 1..m}if exists{i in I} z[i,j] then 1;

set J, := 1..n;


var x{i in I, j in J} binary;

var used{j in J} binary;


minimize obj: sum{j in J}used[j];

s.t. C1 {i in I} :
	sum{j in J}x[i,j] = 1;

s.t. C2 {j in J} :
	sum{i in I}w[i] * x[i,j] <= c * used[j];


