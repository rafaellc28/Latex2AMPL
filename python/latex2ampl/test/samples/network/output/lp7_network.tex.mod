param L, default 2;

param M, := 2 * L + 1;

set I, := 0..M;

set I1, := 0..M - 1;

param nv, := 2 * M * (M + 1);

set A dimen 3, := {i in I, j in I, k in 0..1 : (i < M or k = 1) and (j < M or k = 0)};

param J{(i,j,k) in A}, := if k = 0 then (if j > 0 and j < M then floor((j + 1)/2) else if i > 0 and i < M then (i mod 2) * ((i + 1)/2)) else (if i > 0 and i < M then floor((i + 1)/2) else if j > 0 and j < M then (j mod 2) * ((j + 1)/2));

param Jprev{(i,j,k) in A}, := if k = 1 then (if i < M then J[i,j,0] else J[M - 1,j,1]) else if i > 0 then (if j = M then J[i - 1,M,0] else J[i - 1,j,1]) else if j > 0 then J[M,j - 1,1];


node N {i in I, j in I} :
	net_out = if i = 0 and j = 0 then 10 else if i = M and j = M then -10 else 0;

arc x {(i,j,k) in A} >= 0,
	 from N[i,j], to N[i + 1 - k,j + k];


