#!/home/bulou/virtual/bin/python3
#####!/usr/bin/python3
import re
import numpy
import pandas
from matplotlib import pyplot,ticker
import argparse
import xml.etree.ElementTree as ET
# ##################################################################################################################
def read_data(filename):
    head=pandas.read_csv(filename,nrows=1,header=None)
    entete=head.values[0][0].split()[1:]
    print(entete)
    data=pandas.read_csv(filename,header=0,index_col=False,names=entete, delim_whitespace=True)  #sep=None) #,skiprows=[0],header=None,names=entete)#,header=None,name=[entete])
    print(data)
    return data
# ##################################################################################################################
def read_upf(filename):
    print(filename)
    f=open(filename,"r")
    text=f.readlines()
    f.close()

    input_data = {}
    data_beta = {}
    i=0
    r=numpy.array([])
    rrab=numpy.array([])
    pp_nlcc=numpy.array([])
    pp_local=numpy.array([])
    nbeta=0
    while i < len(text):
        line=text[i]
    #for line in text:
        if "<PP_MESH" in line:
            for field in line.split(): 
                #print(field)
                if "mesh=" in field:
                    if "zmesh=" in field:
                        input_data["Z"]=float(field.split("=")[1].replace('"','').replace('>',''))
                        print("# Z=%f"%(input_data["Z"]))
                    else:
                        input_data["nmesh"]=int(field.split("=")[1].replace('"',''))
                        print("# nmesh=%d"%(input_data["nmesh"]))
                if "dx=" in field:
                    input_data["dx"]=float(field.split("=")[1].replace('"','').replace('>',''))
                    print("# dx= %f"%(input_data["dx"]))
                if "xmin=" in field:
                    input_data["xmin"]=float(field.split("=")[1].replace('"','').replace('>',''))
                    print("# xmin= %f"%(input_data["xmin"]))
                if "rmax=" in field:
                    input_data["rmax"]=float(field.split("=")[1].replace('"','').replace('>',''))
                    print("# rmax= %f"%(input_data["rmax"]))

        if "<PP_R>" in line:
            while "</PP_R>" not in line:
                i+=1
                line=text[i]
                if "</PP_R>" not in line:
                    field=line.split()
                    for val in field:
                        r=numpy.append(r,float(val))
        if "<PP_RAB>" in line:
            while "</PP_RAB>" not in line:
                i+=1
                line=text[i]
                if "</PP_RAB>" not in line:
                    field=line.split()
                    for val in field:
                        rrab=numpy.append(rrab,float(val))
        if "<PP_NLCC" in line:
            while "</PP_NLCC>" not in line:
                i+=1
                line=text[i]
                if "</PP_NLCC>" not in line:
                    field=line.split()
                    for val in field:
                        pp_nlcc=numpy.append(pp_nlcc,float(val))
        if "<PP_LOCAL" in line:
            while "</PP_LOCAL>" not in line:
                i+=1
                line=text[i]
                if "</PP_LOCAL>" not in line:
                    field=line.split()
                    for val in field:
                        pp_local=numpy.append(pp_local,float(val))
        if "<PP_NONLOCAL>" in line:
            while "</PP_NONLOCAL>" not in line:
                i+=1
                line=text[i]
                if "<PP_BETA" in line:
                    nbeta+=nbeta
                    beta=numpy.array([])
                    while "</PP_BETA" not in line:
                        i+=1
                        line=text[i]
                        if "</PP_BETA" not in line:
                            field=line.split()
                            for val in field:
                                beta=numpy.append(beta,float(val))
                data_beta[str(nbeta)]=beta
                del beta
        i+=1
    print(len(r),len(rrab),len(pp_nlcc),len(pp_local),len(pp_nlcc))
    pyplot.plot(r,pp_local)
    pyplot.plot(r,pp_nlcc)
    pyplot.show()
        # section = section.strip().split('\n')
        # if section[0] == 'TEST CONFIGURATIONS':
        #     break
        # elif len(section) >= 2:
        #     keys = re.findall(r'[a-zA-Z0-9()]*[a-zA-Z0-9()]',section[0]) 
        #     if keys[0] == 'n':
        #         keys = ['nn','ll','ff'] 

        #     data = [d.split() for d in section[1:] ]        
        #     if len(data) > 1:
        #         # transpose
        #         m = len(data[0])
        #         datat = []
        #         for j in range(m):
        #             c = []
        #             for r in data:
        #                 c.append(try_float(r[j]))
        #             datat.append(c)    
        #         data = datat
        #     else:
        #         data = [try_float(s) for s in data[0]]
        #     # print(data)

        #     for i,d in enumerate(data):
        #         input_data[keys[i]] = d

    return input_data

# ##################################################################################################################
def read_file(datafile,args,fig,ax):

    
    data=read_data(datafile)
    #data=read_data("ld1ps.wfc")



    print(args.list)
    if len(args.list)>0:
        for tag in args.list:
            ax.plot(data.r,data[tag],label=tag)
            #ax.plot(dataps.r,dataps[tag])
# ##################################################################################################################
def main(args):
    if args.upf is not None:
        for filename in args.upf:
            upf=read_upf(filename)
            #print(upf)
            
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
# #####################################################################################################################
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--files'   ,nargs='+')  # nargs='*' if you want to support the ability to have an empty list.
    parser.add_argument('--upf'   ,nargs='+')  # nargs='*' if you want to support the ability to have an empty list.
    parser.add_argument('--list'   ,nargs='+')  # nargs='*' if you want to support the ability to have an empty list.
    parser.add_argument('--xmax'   ,nargs='?',type=float,default=20.0)
    parser.add_argument('--rcut'   ,nargs='+')
    args = parser.parse_args()
    main(args)

