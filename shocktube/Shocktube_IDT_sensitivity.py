import numpy as np
import matplotlib.pyplot as plt
import time
import pandas as pd
import cantera as ct
import math
import warnings
warnings.filterwarnings("ignore", category=Warning)

#########################################sensitivity analysis for shocktube IDTs################################
######################
#Parameters to modify#
######################
spec = 'C2H4'		#species
equiv = 2.0			#Phi
pressu = 22			#pressure integer
mech = 'gri30'		#mechanism file name (exclude .cti suffix)
tempu = 1000		#list of temperatuers to run
######################

print('Running Cantera ' + ct.__version__ + '\t%s'%mech + '\t%s'%spec + '\tPhi=%.1f'%equiv + '\tP=%iatm'%pressu)

def ignitionDelay(t,p):
    dpdt = np.zeros(t.shape,t.dtype) #1d array
    dt = np.diff(t)
    dp = np.diff(p)
    dpdt[0:-1] = dp/dt
    dpdt[-1] = (p[-1]-p[-2]) / (t[-1]-t[-2])
    i_ign = dpdt.argmax()
    r_ign = t[i_ign]
    return r_ign

reactorPressure = pressu*101325.0 # Pascals 

ideal_gas = ct.Solution('%s.cti'%mech)
nums_of_reactions = ideal_gas.n_reactions
IDT_plus = np.zeros(len(range(ideal_gas.n_reactions)))   
IDT_minus = np.zeros(len(range(ideal_gas.n_reactions)))   
estimatedIgnitionDelayTime = 0.05
STI = pd.DataFrame(data=[], index=ideal_gas.reaction_equations(range(ideal_gas.n_reactions)))
STI["Sensitivities"] = ""
print('Number of reactions to analysis: %i'%nums_of_reactions)

for m in range(ideal_gas.n_reactions):
    ideal_gas.set_multiplier(1.0)
    rxn = ideal_gas.reaction_equations([m])
    print ('current reaction : %s\nTau_plus: %i of %i'%(rxn,m,nums_of_reactions))
    ideal_gas.set_multiplier(2.0,m)
    ideal_gas.TP = tempu, reactorPressure
    ideal_gas.set_equivalence_ratio(phi=equiv, fuel='%s'%spec,oxidizer={'o2':1.0, 'n2':3.76}) # 'air'
    r = ct.Reactor(contents=ideal_gas)
    reactorNetwork = ct.ReactorNet([r])
    
    timeHistory_1 = ct.SolutionArray(ideal_gas, extra=['t'])
    
    t0 = time.time()
    
    t = 0
    counter = 0
    while t < estimatedIgnitionDelayTime:
        t = reactorNetwork.step()
        if not counter % 10:
            timeHistory_1.append(r.thermo.state, t=t)
        counter += 1
    
    tau = ignitionDelay(timeHistory_1.t, timeHistory_1.P)
    t1 = time.time()
    #timeHistory_1.write_csv('.\\timhis.dat',cols=('t','T','P','X'))
    IDT_plus[m] = tau

    
    print('Ignition Delay: {:.3} s for T={}K. Cpu time: {:3.2f}s'.format(IDT_plus[m], tempu, t1-t0))

		
for n in range(ideal_gas.n_reactions):
    ideal_gas.set_multiplier(1.0)
    rxn = ideal_gas.reaction_equations([n])
    print ('current reaction : %s\nTau_minus: %i of %i'%(rxn,n,nums_of_reactions))
    ideal_gas.set_multiplier(0.5,n)
    ideal_gas.TP = tempu, reactorPressure
    ideal_gas.set_equivalence_ratio(phi=equiv, fuel='%s'%spec,oxidizer={'o2':1.0, 'n2':3.76}) # 'air'
    
    r = ct.Reactor(contents=ideal_gas)
    reactorNetwork = ct.ReactorNet([r])
    
    timeHistory_2 = ct.SolutionArray(ideal_gas, extra=['t'])
    
    t0 = time.time()
    
    t = 0
    counter = 0
    while t < estimatedIgnitionDelayTime:
        t = reactorNetwork.step()
        if not counter % 10:
            timeHistory_2.append(r.thermo.state, t=t)
        counter += 1
    
    tau = ignitionDelay(timeHistory_2.t, timeHistory_2.P)
    t1 = time.time()
    #timeHistory_2.write_csv('.\\timhis.dat',cols=('t','T','P','X'))
    IDT_minus[n] = tau
    tempo = math.log(IDT_plus[n]/IDT_minus[n])/math.log(4)
    STI["Sensitivities"][n] = tempo
    print('Ignition Delay: {:.3} s for T={}K. Cpu time: {:3.2f}s'.format(IDT_minus[n], tempu, t1-t0))

STI.to_csv('Sensitivities_IDTs_%s_%ik_%iatm_phi%.1f_%s.csv'%(spec,tempu,pressu,equiv,mech))

STI.sort_values(by=['Sensitivities'],ascending=False,inplace=True)
print(STI.head(10))
STI.sort_values(by=['Sensitivities'],ascending=True,inplace=True)
print(STI.head(10))
