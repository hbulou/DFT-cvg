#####!/home/bulou/virtual/bin/python3
#####!/usr/bin/python3
import numpy
import pandas
from matplotlib import pyplot,ticker
import os.path
#import matplotlib.ticker as ticker
from scipy import constants
Ry = constants.value(u'Rydberg constant times hc in eV')
a0 = constants.value(u'Bohr radius')/1.0e-10
pyplot.rcParams['text.usetex'] = True
import argparse

from sklearn import linear_model

a_exp={'Pd':3.89}
Ecoh_exp={'Pd':-3.89}

##############################################################################################
def plot_cell(data,args):
    fig, ax = pyplot.subplots()
    fig.subplots_adjust(wspace=0, top=0.95, bottom=0.1, left=0.2, right=0.95)

    print("Units: %f %f"%(Ry,a0))
    print('ke_cutoff=%f'%(args.ke)) 
    print('natom=%d'%(args.natom))
    print('ratio=%f'%(args.ratio))
    print('pp=%s'%(args.pp))
    print('nrj<0.0')          
    print('nkpt=%d'%(args.nkpt)) 
    print(args)

    natom=args.natom
    
    for ppfile in args.pp:
        data3=data[
            (data['ke_cutoff']==args.ke)
            & (data['degauss']==args.degauss)
            & (data['natom']==args.natom)
            & (data['ratio']==args.ratio)
            & (data['pp'].str.contains(ppfile))
            & (data['nrj']<0.0)          
            & (data['nkpt']==args.nkpt) 
        ].sort_values(by=['latt_param'])
        #print(data3.head)
        #print(data3.tail)
        #exit()
        ref=data3['nrj'].iloc[-1]
        new_nrj=Ry*data3['nrj'].add(-ref)/natom
        latt_param=a0*data["latt_param"].loc[new_nrj.idxmin()]
        
        print("Comp. Ecoh= %f eV at a0=%f (r0=%f) %s"%(new_nrj.min(),
                                                 latt_param,
                                                 latt_param/numpy.sqrt(2.0),
                                                 ppfile))
        print("Exp Ecoh= %f (%10.2f ) eV at a0_exp=%f (%10.2f) "%(Ecoh_exp['Pd'],
                                                                  100*(new_nrj.min()-Ecoh_exp['Pd'])/Ecoh_exp['Pd'],
                                                                  a_exp['Pd'],
                                                                  100*(latt_param-a_exp['Pd'])/a_exp['Pd'],
                                                                  ))
        
        
        ax.plot(a0*data3['latt_param'],new_nrj,'o-')
        #ax.plot([min(data3['latt_param']),max(data3['latt_param'])], [max(data3['nrj']),max(data3['nrj'])])
        #ax.set_xlabel("Lattice parameter (Bohr radius)")
        #ax.set_ylabel("Total energy (Ry)")
    ax.set_xlabel("Lattice parameter (angstroem)")
    ax.set_ylabel("Total energy (eV)")
    #x1,x2,y1,y2 = pyplot.axis()
    #y2=0.1
    #y1=1.1*new_nrj.min()
    #pyplot.axis((x1,x2,y1,y2))
    # Rewrite the y labels
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%8.3f'))


    pyplot.show()

############################################################################################
def main(args):

    if len(args.data)>0:
        for filename in args.data:
            if os.path.isfile(filename):
                print("Input file %s"%(filename))
                data=pandas.read_csv(filename,sep=' ',
                                     header=None,
                                     usecols=[0,1,2,3,4,5,6,7,8],
                                     names=['namefile','natom','latt_param','ke_cutoff','nrj','ratio','pp','nkpt','degauss'],
                                     dtype={
                                         'namefile':'string',
                                         'natom':'int64',
                                         'latt_param':'float64',
                                         'ke_cutoff':'float64',
                                         'nrj':'float64',
                                         'ratio':'float64',
                                         'pp':'string',
                                         'nkpt':'int64',
                                         'degauss':'float64'
                                     }
                                     )
                #list(data.columns)
                print(data.head)
                print(data.tail)


                pplist=data.pp.unique()
                for ppfile in pplist:
                    print("Pseudopotential file(s): %s"%(ppfile))


                #print(data)
                #print(data.index)
                #print(data.drop_duplicates())
                print(args.plot_ke)






                
                if args.plot_ke:
                    fig, ax = pyplot.subplots()
                    fig.subplots_adjust(wspace=0, top=0.95, bottom=0.1, left=0.2, right=0.95)

                    print("Ploting ke")
                    for ppfile in args.pp:                    
                        data2=data[
                            (data['latt_param']==args.cell)
                            & (data['degauss']==args.degauss)
                            & (data['natom']==args.natom)
                            & (data['ratio']==args.ratio)
                            & (data['pp'].str.contains(ppfile))
                            & (data['nrj']<0.0)
                            & (data['nkpt']==args.nkpt)].sort_values(by=['ke_cutoff'])
                        print(data2['ke_cutoff'],min(data2['nrj']))
                        minnrj=min(data2['nrj'])
                        lab=r'$\varepsilon_0^{min}$ = %8.6f Ry'%(minnrj)
                        ax.plot(data2['ke_cutoff'],data2['nrj']-minnrj,'o-',label=lab)
                        #ax.plot([min(data2['ke_cutoff']),max(data2['ke_cutoff'])], [min(data2['nrj']),min(data2['nrj'])])


                    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%6.2e'))
                    ax.set_xlabel("Kinetic energy cutoff (Ry)")
                    ax.set_ylabel(r"Total energy - $\varepsilon_0^{min}$ (Ry)")
                    ax.legend()
                    pyplot.savefig("ke.png")
                    pyplot.show()


                if args.plot_ratio:
                    fig, ax = pyplot.subplots()
                    fig.subplots_adjust(wspace=0, top=0.95, bottom=0.1, left=0.2, right=0.95)

                    print("Ploting ratio")
                    print(data)
                    for ppfile in args.pp:                    
                        data4=data[
                            (data['latt_param']==args.cell)
                            & (data['degauss']==args.degauss)
                            & (data['natom']==args.natom)
                            & (data['ke_cutoff']==args.ke)
                            & (data['pp'].str.contains(ppfile))
                            & (data['nrj']<0.0)
                            & (data['nkpt']==args.nkpt)].sort_values(by=['ratio'])
                        print("--------------------------------------------------------")
                        print(data4['ratio'])
                        #print((data['ke_cutoff']==args.ke),args.ke)
                        print((data['pp'].str.contains(ppfile)))
                        #print(data4['ratio'],min(data4['nrj']))
                        #exit()
                        minnrj=min(data4['nrj'])
                        lab=r'$\varepsilon_0^{min}$ = %8.6f Ry'%(minnrj)
                        ax.plot(data4['ratio'],data4['nrj']-minnrj,'o-',label=lab)
                        #ax.plot([min(data2['ke_cutoff']),max(data2['ke_cutoff'])], [min(data2['nrj']),min(data2['nrj'])])


                    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%6.2e'))
                    ax.set_xlabel("Kinetic energy cutoff (Ry)")
                    ax.set_ylabel(r"Total energy - $\varepsilon_0^{min}$ (Ry)")
                    ax.legend()
                    pyplot.savefig("ke.png")
                    pyplot.show()






                    
            ######################
            #
            #    Plot_cell
            #
                if args.plot_cell:
                    plot_cell(data,args)

                if args.plot_Ecoh_fill:
                    print("----------------------------------------------------------")
                    f=open("/home/bulou/ownCloud/src/DFT-cvg/README.md",'r+')
                    lines=f.readlines()
                    f.close()
                    df=pandas.DataFrame({"Ecoh":[],"4d":[],"5s":[],"5p":[]})
                    #df.loc[len(df)]={-4.016952
              
                    for line in lines:
                        if ("Ecoh=" in line)&("eV at" in line):
                            ls=line.split()
                            ls6=ls[6].split("_")
                            if len(ls6) > 4:
                                print(ls[6],ls[1],ls6[2].replace("4d",""),ls6[3].replace("5s",""),ls6[4].replace("5p",""))
                                df.loc[len(df)]=[float(ls[1]),float(ls6[2].replace("4d","")),float(ls6[3].replace("5s","")),float(ls6[4].replace("5p",""))]
                    print(df)

                    # create our LinearRegression object
                    lr = linear_model.LinearRegression()
                    predicted = lr.fit(
                        X=df["4d"].values.reshape(-1, 1),
                        y=df["Ecoh"]
                    )
                    print(predicted.coef_)
                    print(predicted.intercept_)
                    Ecoh_exp=-3.89
                    fill4d=(Ecoh_exp-predicted.intercept_)/predicted.coef_
                    print("ideal 4d=%f --> 5s=%f"%(fill4d,10.0-fill4d))
                    fig, ax = pyplot.subplots()
                    fig.subplots_adjust(wspace=0, top=0.95, bottom=0.1, left=0.2, right=0.95)
                    ax.plot(df["4d"],df["Ecoh"],'o-')
                    ax.axhline(y=Ecoh_exp)
                    #ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%6.2e'))
                    ax.set_xlabel("4d filling)")
                    ax.set_ylabel(r"Cohesion energy (eV)")
                    #ax.legend()

                    pyplot.show()
                            

    
##########################################################################
##########################################################################
##########################################################################
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data'   ,nargs='+')  # nargs='*' if you want to support the ability to have an empty list.
    parser.add_argument('--cell'   ,nargs='?',default=10.0,type=float)
    parser.add_argument('--ratio'  ,nargs='?',default=10.0,type=float)
    parser.add_argument('--ke'     ,nargs='?',default=90.0,type=float)
    parser.add_argument('--natom'  ,nargs='?',default=1,type=int)
    parser.add_argument('--pp'     ,nargs='+')
    parser.add_argument('--degauss',nargs='?',default=0.01,type=float)
    parser.add_argument('--nkpt'   ,nargs='?',default=10.0,type=int)
    parser.add_argument('--plot_ke',action='store_true')
    parser.add_argument('--plot_cell',action='store_true')
    parser.add_argument('--plot_ratio',action='store_true')
    parser.add_argument('--plot_Ecoh_fill',action='store_true')
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

