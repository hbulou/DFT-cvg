#!/bin/bash
export LC_NUMERIC="en_US.UTF-8"



############################################################
# Help                                                     #
############################################################
Help()
{
   # Display Help
    echo
    echo "Syntax: submi.sh [--h|run]"
    echo "options:"
    echo "h             Print this Help."
    echo "jobname       jobname"
    echo "cmd           command to run"
    echo "exclude       list of proc to exclude"
    echo
}
ARGUMENT_LIST=(
    "h"
    "jobname"
    "cmd"
    "exclude"
)
# read arguments
opts=$(getopt \
  --longoptions "$(printf "%s:," "${ARGUMENT_LIST[@]}")" \
  --name "$(basename "$0")" \
  --options "" \
  -- "$@"
)
eval set --$opts
jobname="not defined"
cmd=""
exclude=""
while [[ $# -gt 0 ]]; do
    case "$1" in
	--h) # display Help
            Help
	    exit
            #shift 2
	    ;;
	--jobname)
	    jobname=$2
            shift 2
	    ;;
	--cmd)
	    cmd=$2
            shift 2
	    ;;
	--exclude)
	    exclude=$2
            shift 2
	    ;;
	*)
	    break;;
    esac
done
#######################################################################################



#echo $#
#jobname=$1
#$cmd=$2


dd="$(date)"
#newcmd="sbatch --exclude=hpc-n824,hpc-n829,hpc-n830,hpc-n832,hpc-n850 --job-name $jobname $cmd"
#newcmd="sbatch  --exclude=hpc-n524,hpc-n674 --job-name $jobname $cmd"
#newcmd="sbatch  --exclude=hpc-n803,hpc-n727 --job-name $jobname $cmd"


if [ -z "${exclude}" ]
then
    newcmd="sbatch --job-name $jobname $cmd"
    #echo "$exclude is empty"
    #exit
else
    newcmd="sbatch --exclude=$exclude --job-name $jobname $cmd"    
fi



line=`$newcmd`
numjob=`echo $line | awk '{print $4}'`
echo $dd " --- slurm-"$numjob".out --- "$newcmd  >> Logbook.org
tail -1 Logbook.org

# exit

# #numjob=`squeue -u bulou -n $jobname | sort -r -k 1 | head -2 | tail -1 | awk '{print $1}' `
# #numjob=`squeue -u bulou -n $jobname | sort -r -k 1 | head -1 | awk '{print $1}' `
# #echo $dd " --- " $numjob " --- "$cmd  
# #echo $dd " --- slurm-"$numjob".out --- "$newcmd  >> Logbook.org 
# n=`echo $numjob | sed 's/JOBID //'`
# scontrol show job $n > info.$n
# DIRRUN=`pwd`
# echo $DIRRUN " --- " $dd " --- slurm-"$numjob".out --- "$newcmd  >> /home2020/home/ipcms/bulou/Logbook.org
# tail -1 Logbook.org
# #$info #> info.$numjob


# cat >> slurm.hb <<EOF
# &input 
#     &name   ${DIRRUN}/slurm-${numjob}.out
#     &type   slurm
# &end_input
# EOF
