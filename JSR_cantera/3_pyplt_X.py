import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.ticker import FuncFormatter 
##format data
T = np.array([800, 825, 850, 875, 900, 925, 950, 975, 1000, 1025])		# list of temperatuers			    #
species = 'C3H6'
##分析cantera输出的timehistory数据
 
os.makedirs ('./X_%s'%species)

for temperature in T:
    filename = 'timhis_JSR_%dK'%temperature
    xol = pd.read_csv('%s.dat'%filename, engine='python')
    print (xol)
    print (xol.columns)

    fig, ax = plt.subplots(1,1)
    x = xol.columns[0]
    y = xol['%s'%species]
    
    def formatnum(x, pos):
        return '$%.1f$x$10^{-2}$' % (x*100)

    formatter = FuncFormatter(formatnum)

    print ('x col:\n{}'.format(x))
    print ('y col:\n{}'.format(y))
    ax.yaxis.set_major_formatter(formatter)
    ax.set_xlabel("Steps (Tau = 20s)")
    ax.set_ylabel("%s mole fraction"%species)
    plt.title('%s fraction at %d K'%(species,temperature))
    ax.plot(y)
    plt.savefig('.//X_%s//%s_C3H6.png'%(species,filename),dpi=350,format='png')
    plt.show()
