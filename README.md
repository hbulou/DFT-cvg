fichier bash utilisé pour réaliser des calculs DFT avec QE.(adastra - CINES)

# Exemple d'utilisation
## Pour calculer E=f((distance entre deux atomes)
d=2.5 ;  [submit.sh](https://github.com/hbulou/DFT-cvg/blob/main/submit.sh) --jobname d${d} --cmd "./[QE.sh](https://github.com/hbulou/DFT-cvg/blob/main/QE.sh) --type molecule --celldm 20.0 --nkpt 10 --pp H.pbe-kjpaw_psl.1.0.0.UPF --wfccutoff 70.0 --ratiorhowfc 10.0 --elt H --ibrav 1  --totcharge 1.0 --runname mol1 --dmol ${d}"
## Pour un atome seul
### en fonction de la taille de la cellule
acell=10.0 ; submit.sh --jobname acell{acell} --cmd "./QE.sh --type atom --celldm ${acell} --nkpt 10 --pp Co.pbe-spn-kjpaw_psl.0.3.1.UPF --wfccutoff 70.0 --ratiorhowfc 10.0 --elt Co --ibrav 1"

## Analyse des fichiers de sortie

 num=17 ; liste=`etat_jobs.sh --nday 10 --last $num | tail -2 | head -1` ; ~/python_environment/bin/python ~/scripts/HB_QE_Ananlysis.py --nkpt 12 --slurm $liste

## 16/12/2024
### génèse d'un PP pour Pd 4d8.0 5s2.0 5p0.0

n4d=8.0 ; n5s=2.0 ; n5p=0.0 ; submit.sh --jobname pp2 --cmd "gen_PP.sh --pp_filename Pd_4d${n4d}_5s${n5s}_5p${n5p}.UPF --n4d ${n4d} --n5s ${n5s} --n5p ${n5p}"

### cvg avec ke
 ./loop.sh --pp  Pd_4d8.0_5s2.0_5p0.0.UPF --ke 100.0 --ratio 10.0 --loop_ke on

### pour récupérer les data

 num=11 ; liste=`etat_jobs.sh --nday 10 --last $num | tail -2 | head -1` ; ~/python_environment/bin/python ~/scripts/HB_QE_Ananlysis.py --nkpt 12 --slurm $liste

### Pour tracer Etot=f(KE)

python3 ./HB_plot.py --data DFT_cvg_data_Pd.dat --natom 1 --cell 20.0 --ke 100.0 --nkpt 12 --pp Pd_4d8.0_5s2.0_5p0.0.UPF  --degauss 0.01 --ratio 10.0 --plot_ke


### pour calculer Ecoh
 ./loop.sh --pp  Pd_4d8.0_5s2.0_5p0.0.UPF --ke 100.0 --ratio 10.0 --Ecoh on

###  pour extraire les data
  num=51 ; liste=`etat_jobs.sh --nday 10 --last $num | tail -2 | head -1` ; ~/python_environment/bin/python ~/scripts/HB_QE_Ananlysis.py --nkpt 12 --slurm $liste

###   pour afficher Ecoh
  
  python3 ./HB_plot.py --data DFT_cvg_data_Pd.dat --natom 4 --cell 20.0 --ke 100.0 --nkpt 12 --pp Pd_4d8.0_5s2.0_5p0.0.UPF  --degauss 0.01 --ratio 10.0 --plot_cell

### En cours

n4d=9.0 ; n5s=1.0 ; n5p=0.0 ; submit.sh --jobname pp2 --cmd "gen_PP.sh --pp_filename Pd_4d${n4d}_5s${n5s}_5p${n5p}.UPF --n4d ${n4d} --n5s ${n5s} --n5p ${n5p}"
./loop.sh --pp Pd_4d9.0_5s1.0_5p0.0.UPF --ke 100.0 --ratio 10.0 --Ecoh on
n4d=10.0 ; n5s=0.0 ; n5p=0.0 ; submit.sh --jobname pp2 --cmd "gen_PP.sh --pp_filename Pd_4d${n4d}_5s${n5s}_5p${n5p}.UPF --n4d ${n4d} --n5s ${n5s} --n5p ${n5p}"
./loop.sh --pp Pd_4d10.0_5s0.0_5p0.0.UPF --ke 100.0 --ratio 10.0 --Ecoh on

n4d=8.278 ; n5s=1.722 ; n5p=0.0 ; submit.sh --jobname pp2 --cmd "gen_PP.sh --pp_filename Pd_4d${n4d}_5s${n5s}_5p${n5p}.UPF --n4d ${n4d} --n5s ${n5s} --n5p ${n5p}"
./loop.sh --pp Pd_4d8.278_5s1.722_5p0.0.UPF --ke 100.0 --ratio 10.0 --Ecoh on


###   résultats
Ecoh= -4.016952 eV at a0=4.021747 (r0=2.843804) Pd_4d8.0_5s2.0_5p0.0.UPF
Ecoh= -3.561141 eV at a0=4.021747 (r0=2.843804) Pd_4d9.0_5s1.0_5p0.0.UPF
Ecoh= -3.209608 eV at a0=4.021747 (r0=2.843804) Pd_4d10.0_5s0.0_5p0.0.UPF


Ecoh= a * n4d + b --> a=0.455811 et b=-7.66344 (à partir de n4d=8 et n4d=9)
Ecoh=-3.89 (exp) --> n4d=8.2785189
