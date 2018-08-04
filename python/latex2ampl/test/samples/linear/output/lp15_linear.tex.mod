set P;

param b;

param a{j in P};

param c{j in P};

param u{j in P};


var X{j in P};


maximize obj: sum{j in P}c[j] * X[j];

s.t. C1 : sum{j in P}(1 / a[j]) * X[j] <= b;

s.t. C2 {j in P} :
	0 <= X[j] <= u[j];


