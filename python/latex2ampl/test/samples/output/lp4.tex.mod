var alum >= 0;

var silicon >= 0;

var bin5 >= 0;

var bin4 >= 0;

var bin1 >= 0;

var bin3 >= 0;

var bin2 >= 0;


minimize obj: .03 * bin1 + .08 * bin2 + .17 * bin3 + .12 * bin4 + .15 * bin5 + .21 * alum + .38 * silicon;

s.t. C1 : bin1 + bin2 + bin3 + bin4 + bin5 + alum + silicon = 2000;

s.t. C2 : .15 * bin1 + .04 * bin2 + .02 * bin3 + .04 * bin4 + .02 * bin5 + .01 * alum + .03 * silicon <= 60;

s.t. C3 : .03 * bin1 + .05 * bin2 + .08 * bin3 + .02 * bin4 + .06 * bin5 + .01 * alum <= 100;

s.t. C4 : .02 * bin1 + .04 * bin2 + .01 * bin3 + .02 * bin4 + .02 * bin5 <= 40;

s.t. C5 : .02 * bin1 + .03 * bin2 + .01 * bin5 <= 30;

s.t. C6 : .70 * bin1 + .75 * bin2 + .80 * bin3 + .75 * bin4 + .80 * bin5 + .97 * alum >= 1500;

s.t. C7 : 250 <= .02 * bin1 + .06 * bin2 + .08 * bin3 + .12 * bin4 + .02 * bin5 + .01 * alum + .97 * silicon <= 300;

s.t. C8 : 200 >= bin1 >= 0;

s.t. C9 : 2500 >= bin2 >= 0;

s.t. C10 : 800 >= bin3 >= 400;

s.t. C11 : 700 >= bin4 >= 100;

s.t. C12 : 1500 >= bin5 >= 0;

s.t. C13 : alum >= 0;

s.t. C14 : silicon >= 0;


