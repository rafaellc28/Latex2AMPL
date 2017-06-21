set DANGEROUS, := {'Tiger','Lion','Shark','Crocodile'};

set FISH, := {'Goldfish','Guppy','Shark'};

set CATS, := {'Tiger','Lion'};

set DOGS, := {'Beagle','Labrador','Shepherd','Boxer'};

set PETS, := DOGS union CATS union FISH;

set SAFE, := PETS diff DANGEROUS;





solve;


end;
