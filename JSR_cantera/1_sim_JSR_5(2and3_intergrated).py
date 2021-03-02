import pandas as pd
import numpy as np
import time
import cantera as ct
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter 
from threading import Thread
from time import sleep
import warnings
warnings.filterwarnings("ignore", category=Warning)

print("Running Cantera version: {}".format(ct.__version__))
#########################################################################################################################
concentration = 'C3H6:0.0162, O2:0.0681 He:0.9157'																		#
pressu = 1.05 					#pressure integer                                                                       #
mech = 'AramcoMech3.0'			# mechanism file name (exclude .cti suffix)                                             #
T = np.array([800, 825, 850, 875, 900, 925, 950, 975, 1000, 1025])		# list of temperatuers			    #
t_Res = 2.0  					#residenceTime																			#
Vol = 92 						#cm3                                                                                    #
#########################################################################################################################


gas = ct.Solution('%s.cti'%mech)

# reactor parameters
residenceTime = t_Res # s
pressureValveCoefficient = 1e-6
maxPressureRiseAllowed = 1e-9
maxSimulationTime = t_Res*20 # s
reactorPressure = pressu*ct.one_atm  # in atm. This equals 1.06 bars
reactorVolume = Vol*(1e-2)**3  # m3
residenceTime = 2  # s

#########################initialize dataframe#################################################
gas.TPX = T[0],reactorPressure, concentration
fuelAirMixtureTank = ct.Reservoir(gas)
exhaust = ct.Reservoir(gas)

stirredReactor = ct.IdealGasReactor(gas, energy='off', volume=reactorVolume)

massFlowController = ct.MassFlowController(upstream=fuelAirMixtureTank,
                                           downstream=stirredReactor,
                                           mdot=stirredReactor.mass/residenceTime)

pressureRegulator = ct.Valve(upstream=stirredReactor,
                             downstream=exhaust,
                             K=pressureValveCoefficient)

reactorNetwork = ct.ReactorNet([stirredReactor])

columnNames = [stirredReactor.component_name(item) for item in range(stirredReactor.n_vars)]
columnNames = ['pressure'] + columnNames

# Use the above list to create a DataFrame
timeHistory = pd.DataFrame(columns=columnNames)

# Create a DataFrame to store values for the above points
tempDependence = pd.DataFrame(columns=timeHistory.columns)
tempDependence.index.name = 'Temperature'

inletConcentrations = concentration
concentrations = concentration
#######################each T##################################################################
for temperature in T:
    # Re-initialize the gas
    reactorTemperature = temperature  # Kelvin
    reactorPressure = pressu*ct.one_atm  # in atm. This equals 1.06 bars
    reactorVolume = Vol*(1e-2)**3  # m3

    gas.TPX = reactorTemperature, reactorPressure, inletConcentrations

    # Re-initialize the dataframe used to hold values
    timeHistory = pd.DataFrame(columns=columnNames)
    
    # Re-initialize all the reactors, reservoirs, etc.
    fuelAirMixtureTank = ct.Reservoir(gas)
    exhaust = ct.Reservoir(gas)

    # We will use concentrations from the previous iteration to speed up convergence    
    stirredReactor = ct.IdealGasReactor(gas, energy='off', volume=reactorVolume)
    massFlowController = ct.MassFlowController(upstream=fuelAirMixtureTank,
                                               downstream=stirredReactor,
                                               mdot=stirredReactor.mass/residenceTime)
    pressureRegulator = ct.Valve(upstream=stirredReactor, 
                                 downstream=exhaust, 
                                 K=pressureValveCoefficient)
    reactorNetwork = ct.ReactorNet([stirredReactor])
    
    # Re-run the isothermal simulations
    tic = time.time()
    t = 0
    counter = 1
    while t < maxSimulationTime:
        t = reactorNetwork.step()
        if(counter%10 == 0):
             timeHistory.loc[t] = np.hstack([stirredReactor.thermo.P, stirredReactor.mass, 
                   stirredReactor.volume, stirredReactor.T, stirredReactor.thermo.X])
        counter += 1

    state = np.hstack([stirredReactor.thermo.P, stirredReactor.mass, 
                   stirredReactor.volume, stirredReactor.T, stirredReactor.thermo.X])
    toc = time.time()
    print('Simulation Took {:3.2f}s to compute, with {} steps'.format(toc-tic, counter))

    print('Simulation at T={}K took {:3.2f}s to compute'.format(temperature, toc-tic))
    timeHistory.to_csv('.\\timhis_JSR_%dK.dat'%temperature)

    concentrations = stirredReactor.thermo.X
    
    # Store the result in the dataframe that indexes by temperature
    tempDependence.loc[temperature] = state
	
tempDependence.to_csv('jsr_out.out')
########分析cantera输出的timehistory数据
for temperature in T:
    filename = 'timhis_JSR_%dK'%temperature
    #######提取目标物种的浓度数据 以O2 为例
    df = pd.read_csv('%s.dat'%filename,engine='python')
    df_r = pd.DataFrame(data=[],columns = [('X_O2')])

    d1 = df['O2']   #OG OUTPUT
    df_r['X_O2'] = d1  #SORTED FILE
    #print(df_r)
    df_r.to_csv('%s_sorted_O2.csv'%filename)
    #######提取目标物种的浓度数据 以O2 为例
    
    ###绘制目标物种浓度随时间变化图像
    fig, ax = plt.subplots(1,1)
    x = df.columns[0]
    y = df['O2']
    def formatnum(x, pos):
        return '$%.1f$x$10^{-2}$' % (x*100)

    formatter = FuncFormatter(formatnum)

    #print ('x col:\n{}'.format(x))
    #print ('y col:\n{}'.format(y))
    ax.yaxis.set_major_formatter(formatter)
    ax.set_xlabel("Steps (Tau = 20s)")
    ax.set_ylabel("O2 mole fraction")
    plt.title('O2 fraction at %d K'%temperature)
    ax.plot(y)
    plt.savefig('%s.png'%filename,dpi=350,format='png')
    plt.show()

'''
xol = pd.read_csv('timhis_JSR5.dat', engine='python')
print (xol)
print (xol.columns)

xol.plot(y='O2')
plt.savefig('xo2-5.pdf',dpi=350,format='pdf')
plt.show()
'''