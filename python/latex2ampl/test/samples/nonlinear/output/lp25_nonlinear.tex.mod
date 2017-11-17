set I, := 1..2;


var x{i in I} , <= 10, >= -10;


minimize obj: -prod{i in I}sum{j in 1..5}(j * cos((j + 1) * x[i] + j));


