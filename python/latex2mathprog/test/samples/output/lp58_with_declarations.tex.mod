param n integer, >= 2;

set V, := {1..n};

param s symbolic, in V, := 1;

set E dimen 2, within V cross V;

param a{(i,j) in E}, > 0;

param t symbolic, in V, != s, := n;


var flow >= 0;

var x{(i,j) in E} >= 0, <= a[i,j];


maximize obj: flow;

s.t. C1 {i in V} :
	sum{(j,i) in E}x[j,i] + (if i = s then flow else 0), = sum{(i,j) in E}x[i,j] + (if i = t then flow else 0);

s.t. C2 {(i,j) in E} :
	x[i,j], <= a[i,j];


solve;


data;

param n := 0;

set E :=;

param a :=;


end;
