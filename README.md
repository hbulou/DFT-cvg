* essai
  - essai2

|    |                            |    exp.              |                     PBE, kjpaw |
|----|-------------------         |----------------------|--------------------------------|
| Pd | Latt. param.               |   3.89               |   3.952954 (+1.6 %)            |
|    | Cohesion energy (eV/atom)  |  -3.89               |  -3.689025 (-5.2 %)            |


|  Pd                        |    exp.   |                      |                    | Pd_ONCV_PBE-1.0.oncvpsp.upf |
|----------------------------|-----------|---                   |-                   |-|
| 4d                         |           |  9.5                 | 8.0                | 8.0 |
| 5s                         |           |  0.5                 | 2.0                | 2.0 |
| 5p                         |           |  0.0                 | 0.0                | 0.0  |
| fct                        |           |  PBE                 | PBE                | PBE |
| method                     |           |  kjpaw               | kjpaw              |  |
| AE total energy (Ry)       |           |  -10091.748152       | -10091.437760      | |
|  Latt. param.              |   3.89    |   3.952954 (1.62 %)  |  3.952954 (1.62 %) |3.942370 (+1.35 %) |
|  Cohesion energy (eV/atom) |  -3.89    |  -3.689268 (-5.16 %) | -3.813408 (-1.97 %)|-3.703977 (-4.78 %) |


|  Rh                        |    exp.   |                     |                   |                   |                      |
|----------------------------|-----------|---                  |-------------------|-------------------|--------------------- |
| 4d                         |           |  7.0                |8.0                | 9.0               | 9.0                  |
| 5s                         |           |  2.0                |1.0                | 0.0               | 0.0                  |
| 5p                         |           |  0.0                |0.0                | 0.0               | 0.0                  |
| fct                        |           |  PBE                |PBE                | PBE               |   PBESOL             |
| method                     |           |  kjpaw              |kjpaw              | kjpaw             |  kjpaw               |
| AE total energy (Ry)       |           |  -9568.054978       | -9568.237171      | -9568.304006      | -9563.523933         |
|  Latt. param.              |   3.80    |  3.836535 (+1.0 %)  |3.836535  (+1.0 %) | 3.836535 (+1.0 %) | 3.788909 (-0.3 %)    |
|  Cohesion energy (eV/atom) |  -5.75    |  -6.163543 (+7.2 %) |-6.162021 (+7.6 %)  | -6.150323 (+7.0 %) | -7.007016 (+21.9 %)|

Mismatch (ads-sub)/sub
|sub\ads (exp) | Pd  |    Rh   |sub\ads (calc)| Pd  |    Rh|                       
|----|----|----                |---|---    |---|
|Pd  |     0.0  |  -2.3 %      |Pd | 0.0   |  -2.95 %|
|Rh   |   +2.4 % | 0.0         |Rh | +3.0 %||



fichier bash utilisé pour réaliser des calculs DFT avec QE.(adastra - CINES)
============================================================================

# Exemple d'utilisation
* ## Pour calculer E=f((distance entre deux atomes)
d=2.5 ;  [submit.sh](https://github.com/hbulou/DFT-cvg/blob/main/submit.sh) --jobname d${d} --cmd "./[QE.sh](https://github.com/hbulou/DFT-cvg/blob/main/QE.sh) --type molecule --celldm 20.0 --nkpt 10 --pp H.pbe-kjpaw_psl.1.0.0.UPF --wfccutoff 70.0 --ratiorhowfc 10.0 --elt H --ibrav 1  --totcharge 1.0 --runname mol1 --dmol ${d}"
---------------------------
 * **Pour un atome seul:**
  - **en fonction de la taille de la cellule**
acell=10.0 ; submit.sh --jobname acell{acell} --cmd "./QE.sh --type atom --celldm ${acell} --nkpt 10 --pp Co.pbe-spn-kjpaw_psl.0.3.1.UPF --wfccutoff 70.0 --ratiorhowfc 10.0 --elt Co --ibrav 1"

## Analyse des fichiers de sortie

 num=17 ; liste=`etat_jobs.sh --nday 10 --last $num | tail -2 | head -1` ; ~/python_environment/bin/python ~/scripts/HB_QE_Ananlysis.py --nkpt 12 --slurm $liste

#####################################################################################################################################################################
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
  
  python3 ./HB_plot.py --data DFT_cvg_data_Pd.dat --natom 4 --cell 20.0 --ke 100.0 --nkpt 12 --pp Pd_4d8.278_5s1.722_5p0.0_r4d1.6_r5s2.4_r5p2.4.UPF  --degauss 0.01 --ratio 10.0 --plot_cell

### En cours

n4d=9.0 ; n5s=1.0 ; n5p=0.0 ; submit.sh --jobname pp2 --cmd "gen_PP.sh --pp_filename Pd_4d${n4d}_5s${n5s}_5p${n5p}.UPF --n4d ${n4d} --n5s ${n5s} --n5p ${n5p}"
./loop.sh --pp Pd_4d9.0_5s1.0_5p0.0.UPF --ke 100.0 --ratio 10.0 --Ecoh on
n4d=10.0 ; n5s=0.0 ; n5p=0.0 ; submit.sh --jobname pp2 --cmd "gen_PP.sh --pp_filename Pd_4d${n4d}_5s${n5s}_5p${n5p}.UPF --n4d ${n4d} --n5s ${n5s} --n5p ${n5p}"
./loop.sh --pp Pd_4d10.0_5s0.0_5p0.0.UPF --ke 100.0 --ratio 10.0 --Ecoh on

n4d=8.278 ; n5s=1.722 ; n5p=0.0 ; submit.sh --jobname pp2 --cmd "gen_PP.sh --pp_filename Pd_4d${n4d}_5s${n5s}_5p${n5p}.UPF --n4d ${n4d} --n5s ${n5s} --n5p ${n5p}"
./loop.sh --pp Pd_4d8.278_5s1.722_5p0.0.UPF --ke 100.0 --ratio 10.0 --Ecoh on

r4d=1.6 ; r5s=2.4 ; r5p=2.4 ; n4d=8.278 ; n5s=1.722 ; n5p=0.0 ; submit.sh --jobname pp2 --cmd "gen_PP.sh --pp_filename Pd_4d${n4d}_5s${n5s}_5p${n5p}_r4d${r4d}_r5s${r5s}_r5p${r5p}.UPF --n4d ${n4d} --n5s ${n5s} --n5p ${n5p} --r4d ${r4d} --r5s ${r5s} --r5p ${r5p}"

./loop.sh --pp Pd_4d8.278_5s1.722_5p0.0_r4d1.6_r5s2.4_r5p2.4.UPF --ke 100.0 --ratio 10.0 --Ecoh on

exc=PBESOL ; r4d=1.6 ; r5s=2.4 ; r5p=2.4 ; n4d=8.278 ; n5s=1.722 ; n5p=0.0 ; submit.sh --jobname pp2 --cmd "gen_PP.sh --pp_filename Pd_${exc}_4d${n4d}_5s${n5s}_5p${n5p}_r4d${r4d}_r5s${r5s}_r5p${r5p}.UPF --n4d ${n4d} --n5s ${n5s} --n5p ${n5p} --r4d ${r4d} --r5s ${r5s} --r5p ${r5p} --exc ${exc}"

./loop.sh --pp Pd_PBESOL_4d8.278_5s1.722_5p0.0_r4d1.6_r5s2.4_r5p2.4.UPF --ke 100.0 --ratio 10.0 --Ecoh on

###   résultats
Ecoh= -4.016952 eV at a0=4.021747 (r0=2.843804) Pd_4d8.0_5s2.0_5p0.0.UPF
Ecoh= -3.882614 eV at a0=4.021747 (r0=2.843804) Pd_4d8.278_5s1.722_5p0.0.UPF
Ecoh= -3.561141 eV at a0=4.021747 (r0=2.843804) Pd_4d9.0_5s1.0_5p0.0.UPF
Ecoh= -3.209608 eV at a0=4.021747 (r0=2.843804) Pd_4d10.0_5s0.0_5p0.0.UPF
Ecoh= -4.724666 eV at a0=3.968829 (r0=2.806386) Pd_PBESOL_4d8.0_5s2.0_5p0.0_r4d1.6_r5s2.4_r5p2.4.UPF
Ecoh= -4.579386 eV at a0=3.968829 (r0=2.806386) Pd_PBESOL_4d8.278_5s1.722_5p0.0_r4d1.6_r5s2.4_r5p2.4.UPF
Ecoh= -4.232556 eV at a0=3.974121 (r0=2.810128) Pd_PBESOL_4d9.0_5s1.0_5p0.0_r4d1.6_r5s2.4_r5p2.4.UPF


Ecoh= a * n4d + b --> a=0.455811 et b=-7.66344 (à partir de n4d=8 et n4d=9)
Ecoh=-3.89 (exp) --> n4d=8.2785189
