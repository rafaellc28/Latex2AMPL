set INTER;

set exit;

set entr;


node Entr_Int : net_out >= 0;

node Entr_Int : net_in >= 0;

node Intersection {k in INTER diff {entr,exit}};


