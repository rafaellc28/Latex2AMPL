set I;

param a;


var A{i in I} integer >= 0;

var B{i in I} integer >= 0;


minimize obj: if a != 1 then sum{i in I}A[i] else sum{i in I}A[i] + B[i];


