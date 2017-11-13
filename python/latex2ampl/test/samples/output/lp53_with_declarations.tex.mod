set outputs;

set dmus;

set inputs;

param outputdata{td in dmus, o in outputs}, >= 0;

param inputdata{td in dmus, i in inputs}, >= 0;


var theta{td in dmus} >= 0;

var lambda{d in dmus, td in dmus} >= 0;


minimize obj: sum{td in dmus}theta[td];

s.t. C1 {o in outputs, td in dmus} :
	sum{d in dmus}lambda[d,td] * outputdata[d,o] >= outputdata[td,o];

s.t. C2 {i in inputs, td in dmus} :
	sum{d in dmus}lambda[d,td] * inputdata[d,i] <= theta[td] * inputdata[td,i];

s.t. C3 {td in dmus} :
	sum{d in dmus}lambda[d,td] = 1;


