param N;

param Fi{n in 0..N};

param Xi{n in 0..N};


var f;

var s{n in 1..N} >= 0;

var z{n in 1..N} binary;

var x;


maximize obj: f;

s.t. C1 {n in 1..N} :
	s[n], <= z[n];

s.t. C2  : 1, = sum{n in 1..N}z[n];

s.t. C3  : x, = sum{n in 1..N}(Xi[n - 1] * z[n] + (Xi[n] - Xi[n - 1]) * s[n]);

s.t. C4  : f, = sum{n in 1..N}(Fi[n - 1] * z[n] + (Fi[n] - Fi[n - 1]) * s[n]);

s.t. C5 {n in 0..N} :
	Xi[n], >= 0;

s.t. C6 {n in 0..N} :
	Fi[n], >= 0;


solve;


data;

param N := 0;

param Fi :=;

param Xi :=;


end;
