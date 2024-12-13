import numpy
import os.path
import matplotlib.pyplot as plt
import argparse
##########################################################################
##########################################################################
##########################################################################
def get_nfo(file):
    f=open(file,'r+')
    data=f.readlines()
    f.close()
    etot=0.0
    ke_cutoff=0.0
    charge_cutoff=0.0
    latt_param=0.0
    ratio=0.0
    degauss=0.0
    i=0
    nkpt=12
    for line in data:
        if "!    total energy              =" in line:
            etot=float(line.split()[5])
        if "kinetic-energy cutoff     =" in line:
            ke_cutoff=float(line.split()[4])
        if "number of atoms/cell      =" in line:
            natom=int(line.split()[5])
        if "charge density cutoff     =" in line:
            charge_cutoff=float(line.split()[5])
        if "lattice parameter (alat)  =" in line:
            latt_param=float(line.split()[5])
        if "Gaussian smearing, width (Ry)=" in line:
            degauss=float(line.split()[10])
        if "PseudoPot." in line:
            #pp=data[i+1].split("/lus/home/CT9/pcm7459/hbulou/pseudo/")[1]
            pp=data[i+1].split("/")[-1]
        i+=1
    if ke_cutoff != 0.0:
        ratio=charge_cutoff/ke_cutoff
    print(file,natom,latt_param,ke_cutoff,etot,ratio,pp.rstrip(),args.nkpt,degauss)

##########################################################################
##########################################################################
##########################################################################
def main(args):
    if len(args.slurm)>0:
        for file in args.slurm:
            if os.path.isfile(file):
                get_nfo(file)
            else:
                print("# File %s doesn't exist for now"%(file))
##########################################################################
##########################################################################
##########################################################################
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--slurm',nargs='+')  # nargs='*' if you want to support the ability to have an empty list.
    parser.add_argument('--nkpt',nargs='?',default=10,type=int)
    #parser.add_argument('--xyz',nargs='+')  # nargs='*' if you want to support the ability to have an empty list.
    #parser.add_argument('--idx',nargs='+')
    #parser.add_argument('--idxelt',nargs='+')
    args = parser.parse_args()

    # a=numpy.array([0,1,2,3,4,5,6,7,8,9])
    # print(a)
    # print(a.transpose())
    # print(a.reshape(2,5).transpose())
    # exit()
    main(args)
