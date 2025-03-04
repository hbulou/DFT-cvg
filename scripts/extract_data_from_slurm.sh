#!/bin/bash


beg=$1
end=$2
i=$beg

while [ $i -le $end ]; do
    slurm_name="slurm-"$i".out"
    if [ -e $slurm_name ] ; then
	#echo $slurm_name "exist"
	 ~/python_environment/bin/python ~/scripts/HB_QE_Ananlysis.py --nkpt 12 --slurm $slurm_name
    fi
    let "i=$i+1"
done
