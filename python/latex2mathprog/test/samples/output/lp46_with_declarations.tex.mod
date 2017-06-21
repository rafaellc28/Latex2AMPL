param N;

param fi{n in 0..N};

param xi{n in 0..N};


var f;

var x;

var s{n in 1..N} >= 0;

var z{n in 1..N} binary;


maximize obj: f;

s.t. C1 {n in 1..N} :
	s[n], <= z[n];

s.t. C2  : 1, = sum{n in 1..N}z[n];

s.t. C3  : x, = sum{n in 1..N}(xi[n - 1] * z[n] + (xi[n] - xi[n - 1]) * s[n]);

s.t. C4  : f, = sum{n in 1..N}(fi[n - 1] * z[n] + (fi[n] - fi[n - 1]) * s[n]);


solve;


data;

param N := 0;

param fi :=;

param xi :=;


end;
