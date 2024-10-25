fichier bash utilisé pour réaliser des calculs DFT avec QE.

Exemple d'utilisation
d=2.5 ;  submit.sh --jobname d${d} --cmd "./QE.sh --type molecule --celldm 20.0 --nkpt 10 --pp H.pbe-kjpaw_psl.1.0.0.UPF --wfccutoff 70.0 --ratiorhowfc 10.0 --elt H --ibrav 1  --totcharge 1.0 --runname mol1 --dmol ${d}"
