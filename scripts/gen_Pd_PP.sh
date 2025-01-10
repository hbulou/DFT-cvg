#!/bin/bash
#SBATCH --account=pcm7459
#SBATCH --constraint=GENOA
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=0:30:00



ARGUMENT_LIST=(
    "h"
    "pp_filename"
    "elt"
)
# read arguments
opts=$(getopt \
  --longoptions "$(printf "%s:," "${ARGUMENT_LIST[@]}")" \
  --name "$(basename "$0")" \
  --options "" \
  -- "$@"
)
eval set --$opts


pp_filename="HB.UPF"
#pp_filename="Rh.${fct}-spn-kjpaw_psl.0.3.0.UPF"
elt="Rh"
while [[ $# -gt 0 ]]; do
    case "$1" in
	--h) # display Help
            Help
	    exit
            #shift 2
	    ;;
	--pp_filename)
	    pp_filename=$2
            shift 2
	    ;;
	--elt)
	    elt=$2
            shift 2
	    ;;
	*)
	    break;;
    esac
done



fct='PBE'
nrel=1



INPUTFILE="gen_PP.in"
OUTPUTFILE="gen_PP.out"

if [ ${elt} == "Rh" ] ; then
    Z=45.
    n4s=2.0
    n4p=6.0
    n4d=8.0
    n5s=1.0
    n5p=0.0
    cat > $INPUTFILE <<EOF
 &input
   title='${elt}',
   zed=$Z,
   rel=$nrel,
   config='[Kr] 4d${n4d} 5s${n5s} 5p${n5p}',
   iswitch=3,
   dft='$fct'
 /
 &inputp
   lpaw=.true.,
   pseudotype=3,
   file_pseudopw='${pp_filename}',
   author='HB',
   lloc=-1,
   rcloc=1.9,
   which_augfun='PSQ',
   rmatch_augfun_nc=.true.,
   nlcc=.true.,
   new_core_ps=.true.,
   rcore=0.9,
   tm=.true.
 /
6
4S  1  0  ${n4s}  0.00  0.90  1.70  0.0
5S  2  0  ${n5s}  0.00  0.90  1.30  0.0
4P  2  1  ${n4p}  0.00  0.90  1.70  0.0
5P  3  1  ${n5p}  0.00  0.90  1.70  0.0
4D  3  2  ${n4d}  0.00  0.90  1.90  0.0
4D  3  2 -2.00    0.30  0.90  1.90  0.0
EOF
fi
if [ ${elt} == "Pd" ] ; then
    Z=46.
    rcore=2.0
    n4s=2.0
    n4p=6.0
    n4d=9.0
    n5s=1.0
    n5p=0.0
    cat > $INPUTFILE <<EOF
 &input
   title='${elt}',
   zed=$Z,
   rel=$nrel,
   config='[Kr] 4d${n4d} 5s${n5s} 5p${n5p}',
   iswitch=3,
   dft='$fct'
 /
 &inputp
   lpaw=.true.,
   pseudotype=3,
   file_pseudopw='${pp_filename}',
   author='HB',
   lloc=-1,
   rcloc=1.9,
   which_augfun='PSQ',
   rmatch_augfun_nc=.true.,
   nlcc=.true.,
   new_core_ps=.true.,
   rcore=${rcore},
   tm=.true.
 /
6
4S  1  0  ${n4s}  0.00  0.90  2.30  0.0
5S  2  0  ${n5s}  0.00  0.90  1.30  0.0
4P  2  1  ${n4p}  0.00  0.90  1.70  0.0
5P  3  1  ${n5p}  0.00  0.90  1.70  0.0
4D  3  2  ${n4d}  0.00  0.90  1.90  0.0
4D  3  2 -2.00    0.30  0.90  1.90  0.0
EOF
fi

CMD="ld1.x"
if [ $(hostname) == 'pc-hervecal' ] ; then
    echo "this machine is pc-hervecal"
    /home/bulou/ownCloud/src/QE/q-e-develop/bin/$CMD < $INPUTFILE  | tee $OUTPUTFILE
else
    module purge

    module load develop GCC-CPU-3.1.0
    module load quantum-espresso

    module list

    # export OMP_DISPLAY_AFFINITY=TRUE
    export OMP_PROC_BIND=CLOSE
    export OMP_PLACES=THREADS

    export OMP_NUM_THREADS=1





    # MI250 or GENOA or HPDA
    #salloc --account=pcm7459 --constraint=GENOA --job-name="gen_PP" --nodes=1 --time=1:00:00 --exclusive
    srun --ntasks-per-node=1 --cpus-per-task=1 --threads-per-core=1 --label  --  $CMD < $INPUTFILE  | tee $OUTPUTFILE
    #srun --ntasks-per-node=1 --cpus-per-task="${OMP_NUM_THREADS}" --threads-per-core=1 --label  -- $CMD < ${RUNNAME}.in | tee ${RUNNAME}.out
    
fi







