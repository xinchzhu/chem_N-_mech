import numpy as np
import matplotlib.pyplot as plt
import time
import cantera as ct
import warnings
warnings.filterwarnings("ignore", category=Warning)
import os
###############################
mech = 'AramcoMech3.0'
print ('mechnasim file:%s'%mech)
###############################################
print ('reactant to parse: ')
react_n = input()
print ('product to parse:')
prodt_n = input()
print('Running Cantera')
gas1 = ct.Solution('%s.cti'%mech)

def f_reactant():
    n = 0
    for i, r in enumerate(gas1.reactions()):
        if '%s'%react_n in r.reactants:
            print(r)
            rxn_i = i
            rxn_eq = r
            f.write('%s\t%s\n'%(rxn_i+1,rxn_eq ))
            n += 1
    if n == 0:
        print ('no reaction matches!!!')
    
def f_rr():
    n = 0
    for i, r in enumerate(gas1.reactions()):
        if '%s'%react_n in r.reactants and '%s'%prodt_n in r.products:
            print(r)
            rxn_i = i
            rxn_eq = r
            f.write('%s\t%s\n'%(rxn_i+1,rxn_eq ))
            n += 1
    if n == 0:
        print ('no reaction matches!!!')

def f_product():
    n = 0
    for i, r in enumerate(gas1.reactions()):
        if '%s'%prodt_n in r.products:
            print(r)
            rxn_i = i
            rxn_eq = r
            f.write('%s\t%s\n'%(rxn_i+1,rxn_eq ))
            n += 1
    if n == 0:
        print ('no reaction matches!!!')

if __name__ == "__main__":
    f = open('%s_%s.rxn'%(react_n,prodt_n), 'w')
    if len(prodt_n) == 0:
        f_reactant()
    elif len(react_n) == 0:
        f_product()
    else:
        f_rr()
