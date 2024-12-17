#!/usr/bin/python3
###!/home/bulou/virtual/bin/python3


import numpy
import pandas
from matplotlib import pyplot,ticker
import argparse

def read_data(filename):
    head=pandas.read_csv(filename,nrows=1,header=None)
    entete=head.values[0][0].split()[1:]
    print(entete,len(entete))
    for i in range(1,len(entete)):
        if entete[i] in entete[:i-1]:
            entete[i]=entete[i]+str(entete[:i-1].count(entete[i]))
    print(entete,len(entete))

    data=pandas.read_csv(filename,header=0,index_col=False,names=entete, delim_whitespace=True)  #sep=None) #,skiprows=[0],header=None,names=entete)#,header=None,name=[entete])
    print(data)
    return data
def main(args):

    data=read_data("ld1.wfc")
    dataps=read_data("ld1ps.wfc")
    fig, ax = pyplot.subplots()


    print(args.idx)
    if len(args.idx)>0:
        for tag in args.idx:
            ax.plot(data.r,data[tag],label=tag)
            for d in dataps.columns:
                if tag in d:
                    ax.plot(dataps.r,dataps[d],label=d)
                    ax.plot(dataps.r,-dataps[d],label=d)
            
    ax.legend()
    for r in args.rcut:
        print(r)
        pyplot.axvline(x=float(r))
    pyplot.xlim(0, args.xmax)
    #plt.ylim(-1.5, 1.5)
    pyplot.show()
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--idx'   ,nargs='+')  # nargs='*' if you want to support the ability to have an empty list.
    parser.add_argument('--rcut'   ,nargs='+')
    parser.add_argument('--xmax'   ,nargs='?',type=float,default=20.0)  
    args = parser.parse_args()
    main(args)

