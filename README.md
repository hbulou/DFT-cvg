fichier bash utilisé pour réaliser des calculs DFT avec QE.

# Exemple d'utilisation
## Pour calculer E=f((distance entre deux atomes)
d=2.5 ;  [submit.sh](https://github.com/hbulou/DFT-cvg/blob/main/submit.sh) --jobname d${d} --cmd "./[QE.sh](https://github.com/hbulou/DFT-cvg/blob/main/QE.sh) --type molecule --celldm 20.0 --nkpt 10 --pp H.pbe-kjpaw_psl.1.0.0.UPF --wfccutoff 70.0 --ratiorhowfc 10.0 --elt H --ibrav 1  --totcharge 1.0 --runname mol1 --dmol ${d}"
## Pour un atome seul
### en fonction de la taille de la cellule
acell=10.0 ; submit.sh --jobname acell{acell} --cmd "./QE.sh --type atom --celldm ${acell} --nkpt 10 --pp Co.pbe-spn-kjpaw_psl.0.3.1.UPF --wfccutoff 70.0 --ratiorhowfc 10.0 --elt Co --ibrav 1"
