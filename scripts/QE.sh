#!/bin/bash
#SBATCH --account=pcm7459
#SBATCH --constraint=GENOA
#SBATCH --nodes=1
#SBATCH --exclusive
#SBATCH --time=2:00:00

###SBATCH -N 1-4
###SBATCH -n 16
####SBATCH -t 1-00:00:00     


PPDIR="/lus/home/CT9/pcm7459/hbulou/pseudo"
PPDIR="./"

############################################################
# Help                                                     #
############################################################
Help()
{
   # Display Help
   echo "Add description of the script functions here."
   echo
   echo "Syntax: run.sh [--h|celldm|beta|c_on_a|elt|ibrav|nkpt|pp|ratiorhowfc|wfccutoff]"
   echo "options:"
   echo "h               Print this Help."
   echo "beta            (default 0.7)"
   echo "c_on_a            (default 1.0)"
   echo "celldm          (default 7.5 a. u.)"
   echo "elt             (default Pd)"
   echo "ibrav           (default 1)"
   echo "nkpt            (default 10)"
   echo "pp              (default Pd.pbe-n-kjpaw_psl.1.0.0.UPF)"
   echo "ratiorhowfc     (default 10)"
   echo "type            atom|crystal (default crystal)"
   echo "wfccutoff       (default 100.00 Ry)"
   echo "mag"
   echo "degauss(Ry)      (default 0.01 Ry)"
   echo
}
############################################################                                                                                                                                                                                 
# Mass                                                     #                                                                                                                                                                                 
############################################################                                                                                                                                                                                 
set_Mass()
{
    # Base de donnee des masses                                                                                                                                                                                                              
    case ${elt} in
        "H")
            mass=1.007976
            ;;
        "Ti")
            mass=47.867
            ;;
        "Co")
            mass=58.933200
            ;;
	"Ni")
	    mass=58.6934
	    ;;
        "Ru")
            mass=101.07
            ;;
        "Pd")
            mass=106.42
            ;;
        "Rh")
            mass=102.9055
            ;;
        "Ir")
            mass=192.217
            ;;
        "Ru")
            mass=101.07
            ;;
        "Pt")
            mass=195.078
            ;;
        "Au")
            mass=196.966552
            ;;

        *)
            echo "Element not found"
            exit
            break;;
    esac
}
############################################################                                                                                                                                                                                 
# PseudoPotential_chk                                      #                                                                                                                                                                                 
############################################################                                                                                                                                                                                 
PseudoPotential_chk()
{
    # defini le repertoire ou sont stockes les pseudopotentiels                                                                                                                                                                              
    #PPDIR='/usr/local/share/pseudo'
    #    PPDIR='/home/bulou/pseudo'
    #PPDIR='/home2020/home/ipcms/bulou/workdir/pseudo'
    PPDIRPREV=${PPDIR}
    echo "##################################################################"
    echo ${pp_file}
    echo "##################################################################"
    if [ -f ./${pp_file} ] ; then
        PPDIR="../"
        PPDIRPREV="./"
    fi

    if [ ! -f ${PPDIRPREV}/${pp_file} ] ; then
        echo "ERROR - PP file ${PPDIRPREV}/${pp_file} doesn't exist!"
        exit
    fi
    #PPTYPE='unkownPPTYPE'                                                                                                                                                                                                                   
    PPTYPE=`grep "Pseudopotential type"  ${PPDIRPREV}/${pp_file} | sed 's/Pseudopotential type://' | tr -d ' '`
    echo ${PPTYPE}
    case ${PPTYPE} in
        PAW)
            echo "PAW PP"
            ;;
        NC)
            echo "norm conserved PP"
            ;;
        USPP)
            echo "ultrasoft PP"
            ;;
        *)
            echo "not conventionnal PP file"
            Troullier=`grep "Troullier"  ${PPDIRPREV}/${pp_file} | sed 's/Pseudopotential type://' | tr -d ' '`
            if [ -z ${Troullier} ] ; then
                Trouiller=`grep "Trouiller"  ${PPDIRPREV}/${pp_file} | sed 's/Pseudopotential type://' | tr -d ' '`
                if [ -z ${Trouiller} ] ; then
                    pseudo_type=`grep "pseudo_type=" ${PPDIRPREV}/${pp_file} | sed 's/pseudo_type="//' | sed 's/"//g' | tr -d ' '`
                    if [ -z ${pseudo_type} ] ; then
                        echo "Unkown PP TYPE"
                        exit
                    else
                        PPTYPE=${pseudo_type}
                    fi
                else
                    PPTYPE=${Trouiller}
                fi
            else
                PPTYPE=${Troullier}
            fi
            echo "PP TYPE ${PPTYPE}"
           ;;
    esac
}

############################################################
############################################################
# Main program                                             #
############################################################
############################################################



elt="Pd"
type="crystal"
celldm1=7.5
wfccutoff=50.00
beta=0.7
nkpt=10
pp_file=Pd.pbe-n-kjpaw_psl.1.0.0.UPF
ratiorhowfccutoff=10
mass=106.42
ntyp=1
diago='cg'
ibrav=1
celldm2oncelldm1=1.0
celldm3oncelldm1=1.0
dmol=1.0
totcharge=0.0
RUNNAME='rundir'
mag="no"
degauss=0.01
delrundir="no"
# IBRAV
# ibra=1          cubic P (sc)
#      v1 = a(1,0,0),  v2 = a(0,1,0),  v3 = a(0,0,1)
# ibrav=8          Orthorhombic P                  celldm(2)=b/a
#                                             celldm(3)=c/a
#      v1 = (a,0,0),  v2 = (0,b,0), v3 = (0,0,c)



prefix='prefix'





ARGUMENT_LIST=(
    "h"
    "beta"
    "celldm"
    "c_on_a"
    "elt"
    "ibrav"
    "nkpt"
    "pp"
    "prefix"
    "ratiorhowfc"
    "type"
    "wfccutoff"
    "dmol"
    "totcharge"
    "runname"
    "mag"
    "degauss"
    "delrundir"
)
# read arguments
opts=$(getopt \
  --longoptions "$(printf "%s:," "${ARGUMENT_LIST[@]}")" \
  --name "$(basename "$0")" \
  --options "" \
  -- "$@"
)
eval set --$opts

while [[ $# -gt 0 ]]; do
    case "$1" in
	--h) # display Help
            Help
	    exit
            #shift 2
	    ;;
	--beta)
	    beta=$2
            shift 2
	    ;;
	--celldm)
	    celldm1=$2
            shift 2
	    ;;
	--c_on_a)
	    celldm3oncelldm1=$2
            shift 2
	    ;;
	--elt)
	    elt=$2
            shift 2
	    ;;
	--ibrav)
	    ibrav=$2
            shift 2
	    ;;
	--runname)
	    RUNNAME=$2
            shift 2
	    ;;
	--nkpt)
	    nkpt=$2
            shift 2
	    ;;
	--dmol)
	    dmol=$2
            shift 2
	    ;;
	--totcharge)
	    totcharge=$2
            shift 2
	    ;;
	--delrundir)
	    delrundir=$2
            shift 2
	    ;;
	--pp)
	    pp_file=$2
            shift 2
	    ;;
	--prefix)
	    prefix=$2
            shift 2
	    ;;
	--ratiorhowfc)
	    ratiorhowfccutoff=$2
            shift 2
	    ;;
	--type)
	    type=$2
	    shift 2
	    ;;
	--mag)
	    mag=$2
	    shift 2
	    ;;
	--degauss)
	    degauss=$2
	    shift 2
	    ;;
	--wfccutoff)
	    wfccutoff=$2
            shift 2
	    ;;
	*)
	    break;;
    esac
done




module purge

module load develop GCC-CPU-3.1.0
module load quantum-espresso

module list

# export OMP_DISPLAY_AFFINITY=TRUE
export OMP_PROC_BIND=CLOSE
export OMP_PLACES=THREADS

export OMP_NUM_THREADS=1


CMD="pw.x"

PseudoPotential_chk

z=`echo "0.5/${celldm3oncelldm1}" | bc -l`
lx=${celldm1}
lz=`echo "${celldm3oncelldm1}*${celldm1}" | bc -l`
#echo ${celldm1}
#echo ${pp_file_Pd}


mkdir -p ${RUNNAME}
cd ${RUNNAME}

set_Mass



rhocutoff=`echo "$ratiorhowfccutoff*$wfccutoff" | bc -l`

natom=4
if [ $type == "atom" ] ; then
    natom=1
fi
if [ $type == "molecule" ] ; then
    natom=2
fi


cat > ${RUNNAME}.in <<EOF
&control
    calculation = 'scf'
    restart_mode='from_scratch'
    prefix = '${prefix}'
    outdir = './'
    pseudo_dir = '${PPDIR}'
    etot_conv_thr = 1e-5
    forc_conv_thr = 1e-4
    wf_collect=.true.,
    nstep=200
/
&system
    ibrav=${ibrav}
EOF

if [ ${ibrav} -eq 1 ] ; then
cat >> ${RUNNAME}.in <<EOF
    celldm(1) =${celldm1}
EOF
fi

if [ ${ibrav} -eq 8 ] ; then
cat >> ${RUNNAME}.in <<EOF
    celldm(1) =${celldm1}
    celldm(2) =${celldm2oncelldm1}
    celldm(3) =${celldm3oncelldm1}
EOF
fi

cat >> ${RUNNAME}.in <<EOF
    nat=${natom}
    ntyp=${ntyp},
    ecutwfc=${wfccutoff}
    ecutrho=${rhocutoff}
    occupations = 'smearing'
    !  smearing = 'm-p'
    degauss = ${degauss} ,
    ! tot_charge=1.0,
    !nbnd=20
    tot_charge=${totcharge}
EOF

if [ $mag == "yes" ] ; then
    cat >> ${RUNNAME}.in <<EOF
    starting_magnetization(1)=0.0
EOF
fi

cat >> ${RUNNAME}.in <<EOF
    /
&electrons
     mixing_mode='plain',
     mixing_beta=0.7,
     diagonalization='$diago'
     conv_thr=1e-8
     electron_maxstep=1000
/
&ions
/
&cell
/
ATOMIC_SPECIES
  ${elt} ${mass}  ${pp_file}
EOF



if [ $type == "crystal" ] ; then
    cat >> ${RUNNAME}.in <<EOF
ATOMIC_POSITIONS (alat)
  ${elt} 0.0 0.0 0.0 0 0 0
  ${elt} 0.5 0.0 ${z} 0 0 0
  ${elt} 0.5 0.5 0.0 0 0 0
  ${elt} 0.0 0.5 ${z} 0 0 0
K_POINTS (automatic)
  ${nkpt} ${nkpt} ${nkpt} 1 1 1

EOF
fi
if [ $type == "molecule" ] ; then
    cat >> ${RUNNAME}.in <<EOF
ATOMIC_POSITIONS (angstrom)
  ${elt} 0.0 0.0 0.0 0 0 0
  ${elt} ${dmol} 0.0 0.0 0 0 0
K_POINTS (automatic)
  ${nkpt} ${nkpt} ${nkpt} 1 1 1

EOF
fi
	
if [ $type == "atom" ] ; then
    cat >> ${RUNNAME}.in <<EOF
ATOMIC_POSITIONS (alat)
  ${elt} 0.0 0.0 0.0 0 0 0
K_POINTS (automatic)
  ${nkpt} ${nkpt} ${nkpt} 1 1 1

EOF
fi

echo "##########################################################"
cat ${RUNNAME}.in
echo "##########################################################"

srun --ntasks-per-node=192 --cpus-per-task="${OMP_NUM_THREADS}" --threads-per-core=1 --label  -- $CMD < ${RUNNAME}.in | tee ${RUNNAME}.out

if [ $delrundir == "yes" ] ; then
    cd ..
    rm -rf ${RUNNAME}
fi

