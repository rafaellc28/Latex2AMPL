set I, := 1..12;

param a{i in I}, := Uniform(2, 7);

param pos{i in I}, := 1 + card({j in I : a[j] < a[i] or a[j] = a[i] and j < i});

param ind{k in 1..card(I)}, := sum{i in I : pos[i] = k}i;





solve;


end;
