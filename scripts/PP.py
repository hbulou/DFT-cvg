#!/home/bulou/virtual/bin/python3
#####!/usr/bin/python3

import numpy
import pandas
from matplotlib import pyplot,ticker
import argparse

def read_data(filename):
    head=pandas.read_csv(filename,nrows=1,header=None)
    entete=head.values[0][0].split()[1:]
    print(entete)
    data=pandas.read_csv(filename,header=0,index_col=False,names=entete, delim_whitespace=True)  #sep=None) #,skiprows=[0],header=None,names=entete)#,header=None,name=[entete])
    print(data)
    return data


def read_file(datafile,args,fig,ax):

    
    data=read_data(datafile)
    #data=read_data("ld1ps.wfc")



    print(args.list)
    if len(args.list)>0:
        for tag in args.list:
            ax.plot(data.r,data[tag],label=tag)
            #ax.plot(dataps.r,dataps[tag])

def main(args):
    if args.files is not None:
        fig, ax = pyplot.subplots()
        for datafile in args.files:
            read_file(datafile,args,fig,ax)
        
        ax.legend()
        if args.rcut is not None:
            for r in args.rcut:
                print(r)
                pyplot.axvline(x=float(r))

        pyplot.xlim(0, args.xmax)
        pyplot.show()
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--files'   ,nargs='+')  # nargs='*' if you want to support the ability to have an empty list.
    parser.add_argument('--list'   ,nargs='+')  # nargs='*' if you want to support the ability to have an empty list.
    parser.add_argument('--xmax'   ,nargs='?',type=float,default=20.0)
    parser.add_argument('--rcut'   ,nargs='+')
    args = parser.parse_args()
    main(args)

