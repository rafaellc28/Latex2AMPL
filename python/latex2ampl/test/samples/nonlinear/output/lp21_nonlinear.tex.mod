var x{1..3} , >= 0, <= 1;


minimize obj: -32.174 * (255 * log((x[1] + x[2] + x[3] + .03) / (.09 * x[1] + x[2] + x[3] + .03)) + 280 * log((x[2] + x[3] + .03) / (.07 * x[2] + x[3] + .03)) + 290 * log((x[3] + .03) / (.13 * x[3] + .03)));

s.t. C1 : x[1] + x[2] + x[3] = 1;


