import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter 
##format data

filename = 'timhis_JSR_1025'
##分析cantera输出的timehistory数据

xol = pd.read_csv('%s.dat'%filename, engine='python')
print (xol)
print (xol.columns)

fig, ax = plt.subplots(1,1)
x = xol.columns[0]
y = xol['O2']

def formatnum(x, pos):
	return '$%.1f$x$10^{-2}$' % (x*100)

formatter = FuncFormatter(formatnum)

print ('x col:\n{}'.format(x))
print ('y col:\n{}'.format(y))
ax.yaxis.set_major_formatter(formatter)
ax.set_xlabel("Steps (Tau = 20s)")
ax.set_ylabel("O2 mole fraction")
plt.title('O2 fraction')
ax.plot(y)
plt.savefig('%s.pdf'%filename,dpi=350,format='pdf')
plt.show()
