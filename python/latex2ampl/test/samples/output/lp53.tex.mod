set outputs;

set dmus;

set inputs;

param OutputData{td in dmus, o in outputs};

param InputData{td in dmus, i in inputs};


var theta{td in dmus} >= 0;

var lambda{d in dmus, td in dmus} >= 0;


minimize obj: sum{td in dmus}theta[td];

s.t. C1 {o in outputs, td in dmus} :
	sum{d in dmus}lambda[d,td] * OutputData[d,o] >= OutputData[td,o];

s.t. C2 {i in inputs, td in dmus} :
	sum{d in dmus}lambda[d,td] * InputData[d,i] <= theta[td] * InputData[td,i];

s.t. C3 {td in dmus} :
	sum{d in dmus}lambda[d,td] = 1;


