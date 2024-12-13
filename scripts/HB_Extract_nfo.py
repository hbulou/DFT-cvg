#!/usr/bin/python3
import numpy
import matplotlib.pyplot as plt
import argparse
import os
#plt.rcParams['text.usetex'] = True

from scipy.constants import physical_constants

import Atom

a0=physical_constants['Bohr radius'][0]*1.0e10



class function():
    def __init__(self):
        self.x=numpy.array([])
        self.y=numpy.array([])

    def add(self,x,y):
        self.x=numpy.append(self.x,x)
        self.y=numpy.append(self.y,y)

class UnitCell:
    def __init__(self):
        self.natom=0
        self.atoms=numpy.array([])
        self.celldm=numpy.array([1.0,1.0,1.0])
        self.ibrav=-1
        self.ntype=0
        self.type=numpy.array([],int)
        self.T=numpy.zeros((3,3))
        self.Tinv=numpy.zeros((3,3))
        self.box=numpy.zeros(6)
        self.nbonds=0
        self.bonds=numpy.array([])  #numpy.arange(NELTDB*NELTDB).reshape((NELTDB,NELTDB))
    def append(self,Z,x,y,z,idxmol,charge):
        self.natom+=1
        self.atoms=numpy.append(self.atoms,Atom.Atom(self.natom,Z,x,y,z,idxmol,charge))
    def read_configuration(self,file,idxconf,elt='all'):
            f=open(file,'r+')
            data=f.readlines()
            f.close()
            nline=len(data)
            i=0
            current_conf=0
            continue_read=True
            while i < nline and continue_read:
                line=data[i]
                real_natom=0
                if "number of atoms/cell      =" in line:
                    natom=int(line.split()[4])
                if "bravais-lattice index     =" in line:
                    self.ibrav=int(line.split()[3])
                    print("ibrav={:5d}".format(self.ibrav))
                if "celldm(1)=" in line:
                    self.celldm[0]=a0*float(line.split()[1])
                    self.celldm[1]=float(line.split()[3])
                    self.celldm[2]=float(line.split()[5])
                    print("celldm={:12.6f} {:12.6f} {:12.6f}".format(self.celldm[0],self.celldm[1],self.celldm[2]))
                if "ATOMIC_POSITIONS" in line :
                    current_conf+=1
                    if current_conf == idxconf:
                        i+=1
                        for iat in range(natom):
                            line_at=data[i].split()
                            #print(line_at)
                            if "all" in elt:
                                self.append(Atom.elt2Z[line_at[0]],float(line_at[1]),float(line_at[2]),float(line_at[3]),1,0.0)
                                real_natom+=1
                                if len(line_at)==7:
                                    self.atoms[real_natom-1].constraint[0]=int(line_at[4])
                                    self.atoms[real_natom-1].constraint[1]=int(line_at[5])
                                    self.atoms[real_natom-1].constraint[2]=int(line_at[6])
                            elif line_at[0] in elt:
                                self.append(Atom.elt2Z[line_at[0]],float(line_at[1]),float(line_at[2]),float(line_at[3]),1,0.0)
                                real_natom+=1

                            i+=1
                        continue_read=False
                i+=1

            self.set_lattice()
            #for i in range(3):
            #    for j in range(3):
            #        self.T[i][j]=1.0
            self.natom=real_natom
            self.box[0]=self.atoms[0].q[0]
            self.box[1]=self.atoms[0].q[0]
            self.box[2]=self.atoms[0].q[1]
            self.box[3]=self.atoms[0].q[1]
            self.box[4]=self.atoms[0].q[2]
            self.box[5]=self.atoms[0].q[2]
            for i in range(self.natom):
                if self.atoms[i].q[0] < self.box[0]:
                    self.box[0]=self.atoms[i].q[0]
                if self.atoms[i].q[0] > self.box[1]:
                    self.box[1]=self.atoms[i].q[0]
                if self.atoms[i].q[1] < self.box[2]:
                    self.box[2]=self.atoms[i].q[1]
                if self.atoms[i].q[1] > self.box[3]:
                    self.box[3]=self.atoms[i].q[1]
                if self.atoms[i].q[2] < self.box[4]:
                    self.box[4]=self.atoms[i].q[2]
                if self.atoms[i].q[2] > self.box[5]:
                    self.box[5]=self.atoms[i].q[2]
            print(elt)
            print(self.box)
    def set_lattice(self):
        if self.ibrav == 4:
            self.a=self.celldm[0]*numpy.array([1.0,0.0,0.0])
            self.b=self.celldm[0]*numpy.array([-.5,.5*numpy.sqrt(3.0),0.0])
            self.c=self.celldm[0]*self.celldm[2]*numpy.array([0.0,0.0,1.0])
            self.T=numpy.zeros((3,3))
            for i in range(3):
                self.T[0][i]=self.a[i]
                self.T[1][i]=self.b[i]
                self.T[2][i]=self.c[i]
        elif self.ibrav == 8:
            self.a=self.celldm[0]*numpy.array([1.0,0.0,0.0])
            self.b=self.celldm[0]*self.celldm[1]*numpy.array([0.0,1.0,0.0])
            self.c=self.celldm[0]*self.celldm[2]*numpy.array([0.0,0.0,1.0])
            self.T=numpy.zeros((3,3))
            for i in range(3):
                self.T[0][i]=self.a[i]
                self.T[1][i]=self.b[i]
                self.T[2][i]=self.c[i]
        elif self.ibrav == 1:
            self.a=self.celldm[0]*numpy.array([1.0,0.0,0.0])
            self.b=self.celldm[0]*numpy.array([0.0,1.0,0.0])
            self.c=self.celldm[0]*numpy.array([0.0,0.0,1.0])
            self.T=numpy.zeros((3,3))
            for i in range(3):
                self.T[0][i]=self.a[i]
                self.T[1][i]=self.b[i]
                self.T[2][i]=self.c[i]
        else:
            print("#################### WARNING: unkown ibrav={:5d}".format(self.ibrav))
    def save(self,savename):

        if savename.split('.')[-1] == "xyz":

            f=open(savename,"w+")
            f.write(str(self.natom)+"\n")
            f.write(str(self.T[0][0])+" 0.0 0.0 0.0 "+str(self.celldm[1])+" 0.0 0.0 0.0 "+str(self.T[2][2]/self.T[0][0])+" "+str(self.ibrav)+ "\n")
            for i in range(self.natom):
                #f.write(str(Atom.Z2elt[int(self.atoms[i].Z)])+" "+str(self.atoms[i].q[0])+" "+str(self.atoms[i].q[1])+" "+str(self.atoms[i].q[2])+"\n")
                f.write(str(Atom.Z2elt[int(self.atoms[i].Z)])+" "+str(self.atoms[i].q[0])+" "+str(self.atoms[i].q[1])+" "+str(self.atoms[i].q[2])+" "+str(self.atoms[i].constraint[0])+" "+str(self.atoms[i].constraint[1])+" "+str(self.atoms[i].constraint[2])+"\n")

            f.close()
        if savename.split('.')[-1] == "cjson":
            self.Tinv=numpy.linalg.inv(self.T)
            f=open(savename,"w+")
            f.write("{\n")
            f.write("\"chemicalJson\": 0,\n")
            f.write("  \"atoms\": {\n")

            f.write("    \"elements\": {\n")
            f.write("       \"number\": [")
            for i in range(self.natom-1):
                f.write("{:5d},".format(self.atoms[i].Z))
            f.write("{:5d}]\n".format(self.atoms[i].Z))
            f.write("},\n")






            f.write("    \"coords\": {\n")
            f.write("      \"3d\": [")
            for i in range(self.natom-1):
                f.write("{:14.7f}, {:14.7f}, {:14.7f},\n".format(self.atoms[i].q[0],self.atoms[i].q[1],self.atoms[i].q[2]))
            f.write("{:14.7f}, {:14.7f}, {:14.7f} ]\n".format(self.atoms[self.natom-1].q[0],self.atoms[self.natom-1].q[1],self.atoms[self.natom-1].q[2]))
            f.write("}\n")



            f.write("},\n")

            f.write("\"unitCell\": {\n")
            #f.write("  \"a\": {:14.7f},\n".format(self.celldm[0]))
            #f.write("  \"alpha\": 90.0,\n")
            #f.write("  \"b\": {:14.7f},\n".format(self.celldm[0]*self.celldm[1]))
            #f.write("  \"beta\": 90.0,\n")
            #f.write("  \"c\": {:14.7f},\n".format(self.celldm[0]*self.celldm[2]))
            #f.write("  \"gamma\": 90.0\n")
            f.write("  \"cellVectors\": [\n")
            f.write("    {:14.7f},\n".format(self.T[0][0]))
            f.write("    {:14.7f},\n".format(self.T[0][1]))
            f.write("    {:14.7f},\n".format(self.T[0][2]))
            f.write("    {:14.7f},\n".format(self.T[1][0]))
            f.write("    {:14.7f},\n".format(self.T[1][1]))
            f.write("    {:14.7f},\n".format(self.T[1][2]))
            f.write("    {:14.7f},\n".format(self.T[2][0]))
            f.write("    {:14.7f},\n".format(self.T[2][1]))
            f.write("    {:14.7f}\n".format(self.T[2][2]))
            f.write("  ]\n")
                        #f.write(" }\n")
            f.write("}\n")

            f.write("}\n")
            #f.write("       \"3dFractional\": [\n")
            #for i in range(self.natom):
            #    x=0.0 ; y=0.0; z=0.0
            #    for j in range(3):
            #        x=x+self.atoms[i].q[j]*self.Tinv[j][0]
            #        y=y+self.atoms[i].q[j]*self.Tinv[j][1]
            #        z=z+self.atoms[i].q[j]*self.Tinv[j][2]
            #
            #   f.write("{:14.7f},\n{:14.7f},\n{:14.7f},\n".format(x,y,z))
            #f.write("],\n")
            #f.write("},\n")

            #f.write("\"name\": \"XYZ file\",\n")
            #


            f.close()
            print(self.Tinv)
            print(self.T)


        if savename.split('.')[-1] == "xsf":
            f=open(savename,"w+")
            f.write("INFO\n")
            f.write("nunit      1    1    1\n")
            f.write("unit   cell\n")
            f.write("celltype   primcell\n")
            f.write("shape   parapipedal\n")
            f.write(" END_INFO\n")
            f.write(" DIM-GROUP\n")
            f.write("           3           1\n")
            f.write(" PRIMVEC\n")
            f.write("   "+str(self.T[0][0])+"   "+str(self.T[0][1])+"   "+str(self.T[0][2])+"\n")
            f.write("   "+str(self.T[1][0])+"   "+str(self.T[1][1])+"   "+str(self.T[1][2])+"\n")
            f.write("   "+str(self.T[2][0])+"   "+str(self.T[2][1])+"   "+str(self.T[2][2])+"\n")
            f.write(" CONVVEC\n")
            f.write("   "+str(self.T[0][0])+"   "+str(self.T[0][1])+"   "+str(self.T[0][2])+"\n")
            f.write("   "+str(self.T[1][0])+"   "+str(self.T[1][1])+"   "+str(self.T[1][2])+"\n")
            f.write("   "+str(self.T[2][0])+"   "+str(self.T[2][1])+"   "+str(self.T[2][2])+"\n")
            #            f.write(" PRIMVEC\n")
            #            f.write("   "+str(self.celldm[0])+"    0.0000000000    0.0000000000\n")
            #            f.write("    0.0000000000   "+str(self.celldm[1])+"    0.0000000000\n")
            #            f.write("    0.0000000000    0.0000000000   "+str(self.celldm[2])+"\n")
            #            f.write(" CONVVEC\n")
            #            f.write("   "+str(self.celldm[0])+"    0.0000000000    0.0000000000\n")
            #            f.write("    0.0000000000   "+str(self.celldm[1])+"    0.0000000000\n")
            #            f.write("    0.0000000000    0.0000000000   "+str(self.celldm[2])+"\n")
            f.write(" PRIMCOORD\n")
            f.write("          "+str(self.natom)+"           1\n")
            for i in range(self.natom):
                #f.write("  "+str(int(self.atoms[i].Z))+"      "+str(self.atoms[i].q[0])+"     "+str(self.atoms[i].q[1])+"     "+str(self.atoms[i].q[2])+"   0.0 0.0 0.0\n")
                f.write(" {:2d} {:14.7f}{:14.7f}{:14.7f}\n".format(int(self.atoms[i].Z),self.atoms[i].q[0],self.atoms[i].q[1],self.atoms[i].q[2]))
            f.close()

class QE():
    def __init__(self,file):
        self.nconf=0
        self.nscf_cvg=0
        self.ef=0.0
        self.file=file
        print(self.file)
        self.file_info()
    def file_info(self):
        f=open(self.file,'r+')
        data=f.readlines()
        f.close()
        nline=len(data)
        i=0
        self.nconf=0
        self.nscf_cvg=0
        while i < nline:
            line=data[i]
            if "ATOMIC_POSITIONS" in line :
                self.nconf+=1
            if "End of self-consistent calculation" in line :
                self.nscf_cvg+=1
            i+=1
    def get_DOS(self,nscf,text):
        self.KS_nrj=numpy.array([])
        self.KS_nrj_H=numpy.array([])
        self.KS_nrj_L=numpy.array([])
        f=open(self.file,'r+')
        data=f.readlines()
        f.close()
        
        nline=len(data)
        i=0
        iscf_cvg=0
        while i < nline:
            line=data[i]
            if "End of self-consistent calculation" in line :
                iscf_cvg+=1
                nrj=numpy.array([])
                i=i+4 ; line=data[i].split()
                while len(line)>0 :
                    if iscf_cvg == nscf:
                        for j in range(len(line)):
                            self.KS_nrj=numpy.append(self.KS_nrj,float(line[j]))
                    i=i+1
                    line=data[i].split()
                #self.total_energy.x=numpy.append(self.total_energy.x,inrj)
                #self.total_energy.y=numpy.append(self.total_energy.y,float(line.split()[4]))
                #print(self.KS_nrj)
                i=i+1 
                if iscf_cvg == nscf:
                    self.ef=float(data[i].split()[4])

                    for i in range(len(self.KS_nrj)):
                        if self.KS_nrj[i]<=self.ef:
                            self.KS_nrj_H=numpy.append(self.KS_nrj_H,self.KS_nrj[i])
                        else:
                            self.KS_nrj_L=numpy.append(self.KS_nrj_L,self.KS_nrj[i])
                        
                    nbins=numpy.linspace(-8,4,200)

                    #n,b,p=pyplot.hist(self.KS_nrj,bins=nbins,color='red',density=False)
                    #print('-------------------------------------')
                    #print(n)
                    #print(b)
                    #print(n[b[0:-1]>-8])
                    #pyplot.hist(self.KS_nrj,range=(self.KS_nrj.min(),self.ef),bins=nbins,color='red',density=False)
                    #pyplot.hist(self.KS_nrj,range=(self.ef,self.KS_nrj.max()),bins=nbins,color='blue',density=False)
                    nh,bh,ph=pyplot.hist(self.KS_nrj_H,bins=nbins,color='red',density=False)
                    print(nh)
                    print(bh)
                    nl,bl,pl=pyplot.hist(self.KS_nrj_L,bins=nbins,color='blue',density=False)
                    print(nl)
                    print(bl)
                    pyplot.xlabel('Energy (eV)')
                    pyplot.ylabel('Number of KS orbitals')
                    pyplot.title(text)
                    #pyplot.xlim(-10, 5)
                    #pyplot.ylim(0, 35)
                    pyplot.grid(True)
                    pyplot.show()
            i=i+1
        

    def get_total_energy(self,plot=False):
        self.total_energy=function()
        f=open(self.file,'r+')
        data=f.readlines()
        f.close()
        nline=len(data)
        i=0
        inrj=0
        while i < nline and inrj<self.nconf:
            line=data[i]
            if "!" in line :
                inrj+=1
                #print(inrj,line.split()[4],self.nconf)

                self.total_energy.x=numpy.append(self.total_energy.x,inrj)
                self.total_energy.y=numpy.append(self.total_energy.y,float(line.split()[4]))

            i+=1
        if plot:
            plt.plot(self.total_energy.x,self.total_energy.y)
            plt.xlabel('Step')
            plt.ylabel('Total Energy')
            plt.show()
    def view(self):
        conf1=UnitCell()
        self.file_info()
        conf1.read_configuration(self.file,self.nconf)
        conf1.save("jmol.xyz")
        os.system("jmol jmol.xyz")



##########################################################################
##########################################################################
##########################################################################
def main(args):
    slurm=QE("slurm.out")
    slurm.file_info()
    print(slurm.nconf)
    slurm.get_total_energy(plot=True)
    print(slurm.total_energy.y)
    slurm.view()
##########################################################################
##########################################################################
##########################################################################
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    #parser.add_argument('--traj',nargs='+')  # nargs='*' if you want to support the ability to have an empty list.
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

