set I, := 1..5;


var x{i in I} , <= 0.4, >= -0.5, := .4;


minimize obj: sum{i in I}x[i] ^ 10;


