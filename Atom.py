

elt2Z = {"H": 1, "C": 6, "Ca": 20, "O": 8, "N": 7, "Na":11, "P": 15, "Cl" : 17, "Ti": 22, "Cu": 29,"Br":35,"Ru":44,"Rh":45,"Pd":46,"Ir":77,"Pt":78,"Ag":47,"Au":79}
Z2elt = {1: "H", 6: "C", 20: "Ca", 8: "O", 7: "N", 11:"Na", 15:"P" ,17:"Cl", 22:"Ti", 29:"Cu", 35:"Br",
         44:"Ru",45:"Rh",46:"Pd",77:"Ir",78:"Pt",
         47:"Ag",79:"Au"}
mass  = {"H": 1.007978,"C":12.0106,"Ca":40.078,"Cl":35.4527, "O":15.99940,"N":14.006855,"Na":22.989770, "P":30.973762,"Ti":47.867,"Cu":63.546,"Br":79.904,
         "Ru":101.07,"Rh":102.905504,"Pd":106.42,"Ir":192.216,"Pt":195.080,
         "Ag":107.8682,"Au":196.96657}

import numpy
class Atom:

    def __init__(self, idx, Z, x, y, z, idxmol, charge):
        print(type(Z))
        self.idx = idx
        #self.Z = Z
        #self.elt = Atom.Z2elt[Z]
        if isinstance(Z,int):
        #if type(Z) == int:
            self.Z = Z
            self.elt = Z2elt[Z]
        else:
            self.Z = elt2Z[Z]
            self.elt = Z

        self.charge = charge
        self.q = numpy.array([x, y, z])
        self.constraint = numpy.array([1,1,1])
        self.idxmol = idxmol
        self.voisin=numpy.array([])
        self.nvoisin=0
    class Voisin:
        def __init__(self,idx,r,dx,dy,dz):
            self.idx=idx
            self.r=r
            self.dr=numpy.array([dx,dy,dz])
        

    def copy(self,src,idxmol):
        self.idx = src.idx
        self.Z = src.Z
        self.charge = src.charge
        self.q = numpy.array([src.q[0], src.q[1], src.q[2]])
        self.idxmol = idxmol
