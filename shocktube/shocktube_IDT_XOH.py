import numpy as np
import matplotlib.pyplot as plt
import time
import cantera as ct
import warnings
warnings.filterwarnings("ignore", category=Warning)

######################
#Parameters to modify#
######################
spec = 'C2H4'	#species
equiv = 1.0		#Phi
pressu = 30 	#pressure integer
mech = 'AramcoMech3.0'		# mechanism file name (exclude .cti suffix)
T_r = np.array([1055.8, 1108.9, 1151, 1201, 1250.4])		# list of temperatuers to run
######################

print('Running Cantera ' + ct.__version__ + '\t%s'%mech + '\t%s'%spec + '\tPhi=%.1f'%equiv + '\tP=%iatm'%pressu)

'''
def ignitionDelay(t,p):
	dpdt = np.zeros(t.shape,t.dtype) #1d array
	dt = np.diff(t)
	dp = np.diff(p)
	dpdt[0:-1] = dp/dt
	dpdt[-1] = (p[-1]-p[-2]) / (t[-1]-t[-2])
	i_ign = dpdt.argmax()
	r_ign = t[i_ign]
	return r_ign
'''
def ignitionDelay(states, species):
    i_ign = states(species).Y.argmax()
    return states.t[i_ign]

reactorPressure = pressu*101325.0 # Pascals 

ideal_gas = ct.Solution('%s.cti'%mech)
IDTs = np.zeros(len(T_r))   
estimatedIgnitionDelayTimes = np.ones(len(T_r))
estimatedIgnitionDelayTimes[:] = 0.05

for i, tempu in enumerate(T_r):
    ideal_gas.TP = tempu, reactorPressure
    ideal_gas.set_equivalence_ratio(phi=equiv, fuel='%s'%spec,
                                oxidizer={'o2':1.0, 'n2':3.76}) # 'air'
    r = ct.Reactor(contents=ideal_gas)
    reactorNetwork = ct.ReactorNet([r])

    timeHistory = ct.SolutionArray(ideal_gas, extra=['t'])

    t0 = time.time()

    t = 0
    counter = 0
    while t < estimatedIgnitionDelayTimes[i]:
        t = reactorNetwork.step()
        if not counter % 10:
            timeHistory.append(r.thermo.state, t=t)
        counter += 1

    tau = ignitionDelay(timeHistory, 'oh')
    t1 = time.time()
    timeHistory.write_csv('.\\timhis.dat',cols=('t','T','P','X'))
    IDTs[i] = tau
    print('Ignition Delay: {:.3} ms for T={}K. Cpu time: {:3.2f}s'.format(tau*1000, tempu, t1-t0))

out = open('IDTs(XOH)_%s_Phi%.1f_P%i.out'%(spec,equiv,pressu),'w')
out.write('p\tT\t1000/T\tidt(s)\n')
for i, T in enumerate(T_r):
	over_T = 1000.0 / T
	out.write('%i\t%f\t%f\n'%(T,over_T,IDTs[i]*1000))
out.close()



