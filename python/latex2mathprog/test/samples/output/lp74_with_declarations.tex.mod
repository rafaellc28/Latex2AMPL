param R, := 2;

param file symbolic, := "graph.eps";

param n integer, > 0;

set V, default 1..n;

param y{i in V}, default 50 * sin((i - 1) / card(V) * 8 * atan(1));

param x{i in V}, default 50 * cos((i - 1) / card(V) * 8 * atan(1));

set E, within V cross V;

param y1, := (max{i in V}y[i]) + R + 3.0;

param y0, := (min{i in V}y[i]) - R - 3.0;

param x0, := (min{i in V}x[i]) - R - 3.0;

param x1, := (max{i in V}x[i]) + R + 3.0;





solve;


data;

param n := 0;

set V :=;

param y :=;

param x :=;

set E :=;


end;
