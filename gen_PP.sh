#!/bin/bash
#SBATCH --account=pcm7459
#SBATCH --constraint=GENOA
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=0:30:00

ARGUMENT_LIST=(
    "h"
    "pp_filename"
    "n4d"
    "n5s"
    "n5p"
)
# read arguments
opts=$(getopt \
  --longoptions "$(printf "%s:," "${ARGUMENT_LIST[@]}")" \
  --name "$(basename "$0")" \
  --options "" \
  -- "$@"
)
eval set --$opts


pp_filename="PP.UPF"

n4d=9.0
n5s=1.0
n5p=0.0

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
	--n4d)
	    n4d=$2
            shift 2
	    ;;
	--n5s)
	    n5s=$2
            shift 2
	    ;;
	--n5p)
	    n5p=$2
            shift 2
	    ;;
	*)
	    break;;
    esac
done


elt='Pd'
Z=46


INPUTFILE="gen_PP.in"
OUTPUTFILE="gen_PP.out"
cat > $INPUTFILE <<EOF
     &input	     
    zed=$Z.,
    title='${elt}',
    rel=1,
    config='[Kr] 4d${n4d} 5s${n5s} 5p${n5p}',
    iswitch=3,
    dft='PBE'
 /
 &inputp
   lloc=0,
   file_pseudopw='${pp_filename}',
   pseudotype=3,
   nlcc=.true.,
   rcore=0.9,
   author='HB',
 /
3
5P  2  1  ${n5p}  0.00  2.40  2.40  1
4D  3  2  ${n4d}  0.00  1.80  2.40  1
5S  1  0  ${n5s}  0.00  2.40  2.40  1
EOF


module purge

module load develop GCC-CPU-3.1.0
module load quantum-espresso

module list

# export OMP_DISPLAY_AFFINITY=TRUE
export OMP_PROC_BIND=CLOSE
export OMP_PLACES=THREADS

export OMP_NUM_THREADS=1


CMD="ld1.x"


# MI250 or GENOA or HPDA
#salloc --account=pcm7459 --constraint=GENOA --job-name="gen_PP" --nodes=1 --time=1:00:00 --exclusive
srun --ntasks-per-node=1 --cpus-per-task=1 --threads-per-core=1 --label  --  $CMD < $INPUTFILE  | tee $OUTPUTFILE
#srun --ntasks-per-node=1 --cpus-per-task="${OMP_NUM_THREADS}" --threads-per-core=1 --label  -- $CMD < ${RUNNAME}.in | tee ${RUNNAME}.out



