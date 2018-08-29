set c_raw;

set m_pos dimen 2;

param util_pct, := 0.85;

set center;

set region;

set c_final;

set nutr;

set p_cap, dimen 2;

param exch, := 0.4;

set cc_pos dimen 2;

set cp_pos dimen 2;

set proc;

set unit;

set c_inter;

set plant, within center;

set port, within center;

set c_ship, within c_inter;

set commod, := c_final union c_inter union c_raw;

set p_except, within proc cross plant;

param util{u in unit, pc in proc}, >= 0;

param p_imp{cm in commod}, >= 0;

param p_pr{p in plant, cr in c_raw}, >= 0;

param impd_barg{p in plant}, >= 0;

param dcap{p in plant, u in unit}, >= 0;

param road{r in region, c in center}, >= 0;

param io{c in commod, p in proc};

param impd_road{p in plant}, >= 0;

param rail_half{p in plant, plant}, >= 0;

param p_r{cr in c_raw}, >= 0;

param fn{cf in c_final, n in nutr}, >= 0;

param cf75{r in region, cf in c_final}, >= 0;

param tran_import{r in region, po in port}, := if road[r,po] > 0 then (.5 + .0144 * road[r,po]) else 0;

param tran_final{pl in plant, r in region}, := if road[r,pl] > 0 then (.5 + .0144 * road[r,pl]) else 0;

param rail{p1 in plant, p2 in plant}, := rail_half[p1,p2] + rail_half[p2,p1];

param icap{u in unit, pl in plant}, := 0.33 * dcap[pl,u];

param p_dom{pl in plant, c in c_raw}, := if p_r[c] > 0 then p_r[c] else p_pr[pl,c];

param cn75{r in region, n in nutr}, := sum{c in c_final}cf75[r,c] * fn[c,n];

param tran_raw{pl in plant}, := (if impd_barg[pl] > 0 then (1.0 + .0030 * impd_barg[pl]) else 0) + (if impd_road[pl] > 0 then (0.5 + .0144 * impd_road[pl]) else 0);

set p_pos dimen 2, := p_cap diff p_except;

param tran_inter{p1 in plant, p2 in plant}, := if rail[p1,p2] > 0 then (3.5 + .03 * rail[p1,p2]) else 0;


var Psil;

var Psii;

var Psip;

var Xi{(c,p1) in cp_pos, p2 in plant : (c,p1) in cp_pos and (c,p2) in cc_pos}, >= 0;

var Vf{cf in c_final, r in region, p in port}, >= 0;

var Xf{(c,pl) in cp_pos, r in region : (c,pl) in cp_pos}, >= 0;

var Vr{(c,pl) in cc_pos : (c,pl) in cc_pos}, >= 0;

var U{(c,pl) in cc_pos : (c,pl) in cc_pos}, >= 0;

var Z{pr in proc, pl in plant}, >= 0;


minimize obj: Psip + Psil + Psii;

s.t. C1 {n in nutr, r in region} :
	sum{c in c_final}fn[c,n] * (sum{po in port}Vf[c,r,po] + sum{pl in plant : (c,pl) in cp_pos}Xf[c,pl,r]) >= cn75[r,n];

s.t. C2 {c in c_final, r in region : cf75[r,c] > 0} :
	sum{po in port}Vf[c,r,po] + sum{pl in plant : (c,pl) in cp_pos}Xf[c,pl,r] >= cf75[r,c];

s.t. C3 {c in commod, pl in plant} :
	sum{pr in proc : (pr,pl) in p_pos}io[c,pr] * Z[pr,pl] + (if (c in c_ship) then sum{p2 in plant}((if (c,p2) in cp_pos and (c,pl) in cc_pos then Xi[c,p2,pl]) - (if (c,p2) in cc_pos and (c,pl) in cp_pos then Xi[c,pl,p2]))) + (if (c in c_raw and (c,pl) in cc_pos) then ((if p_imp[c] > 0 then Vr[c,pl]) + (if p_dom[pl,c] > 0 then U[c,pl]))) >= if (c in c_final and (c,pl) in cp_pos) then sum{r in region}Xf[c,pl,r];

s.t. C4 {(u,pl) in m_pos} :
	sum{pr in proc : (pr,pl) in p_pos}util[u,pr] * Z[pr,pl] <= util_pct * icap[u,pl];

s.t. C5 : Psip = sum{(c,pl) in cc_pos : c in c_raw}p_dom[pl,c] * U[c,pl];

s.t. C6 : Psil = sum{c in c_final}(sum{pl in plant, r in region : (c,pl) in cp_pos}tran_final[pl,r] * Xf[c,pl,r] + sum{po in port, r in region}tran_import[r,po] * Vf[c,r,po]) + sum{c in c_ship, p1 in plant, p2 in plant : (c,p1) in cp_pos and (c,p2) in cc_pos}tran_inter[p1,p2] * Xi[c,p1,p2] + sum{c in c_raw, pl in plant : (c,pl) in cc_pos and p_imp[c] > 0}tran_raw[pl] * Vr[c,pl];

s.t. C7 : Psii/exch = sum{c in c_final, r in region, po in port}p_imp[c] * Vf[c,r,po] + sum{c in c_raw, pl in plant : (c,pl) in cc_pos}p_imp[c] * Vr[c,pl];


