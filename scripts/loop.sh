#!/bin/bash

elt="Pd"
pp="PP.UPF"


#########################################################################
ARGUMENT_LIST=(
    "h"
    "pp"
    "ke"
    "ratio"
    "Ecoh"
    "loop_ke"
    "loop_ratio"
    "test"
)
# read arguments
opts=$(getopt \
  --longoptions "$(printf "%s:," "${ARGUMENT_LIST[@]}")" \
  --name "$(basename "$0")" \
  --options "" \
  -- "$@"
)
eval set --$opts


ke0=100.0
while [[ $# -gt 0 ]]; do
    case "$1" in
	--h) # display Help
            Help
	    exit
            #shift 2
	    ;;
	--pp)
	    pp=$2
            shift 2
	    ;;
	--ke)
	    ke0=$2
            shift 2
	    ;;
	--ratio)
	    ratio0=$2
            shift 2
	    ;;
	--Ecoh)
	    calc_Ecoh=$2
	    shift 2
	    ;;
	--test)
	    test_script=$2
	    shift 2
	    ;;
	--loop_ke)
	    loop_ke=$2
	    shift 2
	    ;;
	--loop_ratio)
	    loop_ratio=$2
	    shift 2
	    ;;
	*)
	    break;;
    esac
done

###################################################################
loop()
{
    for ke in $(seq $ke_beg $dke $ke_end) ; do
	for ratio in $(seq $ratio_beg $dratio $ratio_end) ; do
	    for cell in $(seq $cell_beg $dcell $cell_end) ; do
		for nkpt in $(seq $nkpt_beg $dnkpt $nkpt_end) ; do
		    submit.sh  --jobname rundir${rundir}  --cmd "./QE.sh --type ${type} --celldm ${cell} --nkpt ${nkpt} --pp ${pp} --wfccutoff ${ke} --ratiorhowfc ${ratio} --elt ${elt} --ibrav 1 --runname rundir${rundir} --delrundir ${delrundir}"
		    let "rundir=rundir+1"
		done
	    done
	done
    done
}



################################################################
test_script(){

    type='crystal'

    ke_beg=${ke0}         ; dke=10.0      ;  ke_end=${ke_beg}
    ratio_beg=${ratio0}   ; dratio=10.0   ;  ratio_end=${ratio_beg}
    nkpt_beg=12           ; dnkpt=10    ;  nkpt_end=${nkpt_beg}


    cell_beg=7.5  ; dcell=0.2  ; cell_end=7.6

    loop
}

################################################################
Ecoh(){

    type='crystal'

    ke_beg=${ke0}         ; dke=10.0      ;  ke_end=${ke_beg}
    ratio_beg=${ratio0}   ; dratio=10.0   ;  ratio_end=${ratio_beg}
    nkpt_beg=12           ; dnkpt=10    ;  nkpt_end=${nkpt_beg}

    
    cell_beg=7.0  ; dcell=0.1  ; cell_end=7.3
    loop
    cell_beg=7.31  ; dcell=0.01  ; cell_end=7.59
    loop
    cell_beg=7.6  ; dcell=0.1  ; cell_end=9.9
    loop
    cell_beg=10.0  ; dcell=1.0  ; cell_end=30.0
    loop
}



################################################################
init_loop_limits(){
    type='atom'

    ke_beg=40.0   ; dke=10.0   ; ke_end=200.0
    cell_beg=8.0  ; dcell=1.0  ; cell_end=40.0
    ratio_beg=2.0 ; dratio=1.0 ; ratio_end=12.0
    nkpt_beg=12   ; dnkpt=1 ; nkpt_end=20
}
################################################################
ke(){
    init_loop_limits
    #ke_beg=100.0    ; ke_end=${ke_beg}
    ratio_beg=${ratio0} ; ratio_end=${ratio_beg}
    cell_beg=20.0  ; cell_end=${cell_beg}
    nkpt_beg=12    ; nkpt_end=${nkpt_beg}
    loop
}
################################################################
ratio(){
    init_loop_limits
    ke_beg=${ke0}    ; ke_end=${ke_beg}
    #ratio_beg=10.0 ; ratio_end=${ratio_beg}
    cell_beg=20.0  ; cell_end=${cell_beg}
    nkpt_beg=12    ; nkpt_end=${nkpt_beg}
    loop
}
################################################################
cell(){
    init_loop_limits
    ke_beg=${ke0}    ; ke_end=${ke_beg}
    ratio_beg=${ratio0} ; ratio_end=${ratio_beg}
    #cell_beg=20.0  ; cell_end=${cell_beg}
    nkpt_beg=12    ; nkpt_end=${nkpt_beg}
    loop
}
################################################################
nkpt(){
    init_loop_limits
    ke_beg=${ke0}    ; ke_end=${ke_beg}
    ratio_beg=10.0 ; ratio_end=${ratio_beg}
    cell_beg=20.0  ; cell_end=${cell_beg}
    #nkpt_beg=12    ; nkpt_end=${nkpt_beg}
    loop
}


#####################################################################
#####################################################################
#####################################################################

delrundir="yes"
rundir=1


if ! [ -z ${loop_ke} ] ; then
    echo "loop on ke OK"
    ke
else
    echo "no loop on ke"
fi
if ! [ -z ${loop_ratio} ] ; then
    echo "loop on ratio OK"
    ratio
else
    echo "no loop on ratio"
fi
if ! [ -z ${calc_Ecoh} ] ; then
    echo "loop on Ecoh OK"
    Ecoh
else
    echo "no loop on Ecoh"
fi
if ! [ -z ${test_script} ] ; then
    echo "test script OK"
    test_script
else
    echo "no test script"
fi
#ke

# for Ecoh=f(e)
#Ecoh






#cell_beg=9.0  ; dcell=1.0  ; cell_end=30.0
#pp='Au.pbe-rrkj-9.0-2.0.UPF' 
#loop
#pp='Au.pbe-rrkj-9.5-1.5.UPF'
#loop
#pp='Au.pbe-rrkj-10.0-1.0.UPF'
#loop
