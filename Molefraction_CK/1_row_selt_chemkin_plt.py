import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.ticker import FuncFormatter 

T = np.array([800, 850, 875, 900, 925, 950, 975, 1000, 1025, 1050, 1075, 1100])		# list of temperatuers			    #

No_of_runs = len(T)
print ('No. of runs:%d' %No_of_runs)

df = pd.read_csv('export_contour.plt',delim_whitespace = True, header=None, names=['Temp','time','X_O2'])
#df_r = pd.DataFrame(data=[],columns = ('Temp','time','X_O2'))
print(df)
#df_r = df_r.append(df.iloc[0]) ##1st row

for temperature in T:
    df_r = pd.DataFrame(data=[],columns = ('Temp','time','X_O2'))
    temp_i =  int (np.argwhere(T==temperature))  #确定nparray数组索引
    for i in range(1,len(df)):
        if i % No_of_runs == 0:
            i_n = i + temp_i
            df_r = df_r.append(df.iloc[i_n])
    
    print (df_r)
    i = 0
    df_r.to_csv('%dK.csv'%temperature)
	
for temperature in T:
    file = '%dK'%temperature
    suffix = '.csv'
    filename = '%s%s'%(file,suffix)
    #def suffix = '.dat'
    
    #print ('%s'%file+'%s'%suffix)
    #print ('%s%s'%(file,suffix))
    #print ('%s'%filename)
    #xol_1 = pd.read_csv('O2_800K.csv', engine='python')
    xol = pd.read_csv('%s'%filename, engine='python')
    #print (xol)
    print (xol.columns)
    
    x = xol['time']
    y = xol['X_O2']
    fig, ax = plt.subplots(1,1)
    def formatnum(x, pos):
        return '$%.1f$x$10^{-2}$' % (x*100)
    
    formatter = FuncFormatter(formatnum)
    
    print ('x col:\n{}'.format(x))
    print ('y col:\n{}'.format(y))
    ax.yaxis.set_major_formatter(formatter)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("O2 mole fraction")
    plt.title('O2 fraction at %dK'%temperature)
    ax.plot(x,y)
    #xol.plot(x='Time Run#1_(sec)',y='Mole fraction O2 Run#1')
    plt.savefig('%s.png'%file,dpi=350,format='png')
    plt.show()
