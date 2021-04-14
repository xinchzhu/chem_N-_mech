import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

T=600
kb = 1.381e-23
h = 6.62607015e-34
c = 3e10

v_freq = pd.read_csv('freq.dat', header=None, engine='python')
f_out = open('freq.out', 'a')
qvib = 1
for i in range(0, len(v_freq)):
    qvib = qvib * 1/(1-np.exp(-h*c*v_freq.iloc[i,0]/kb/T))
    #print (v_freq.iloc[i,0])
    #print (qvib)
#print (qvib)
f_out.write ('%d\t%f.2\n'%(T,qvib))
f_out.close()

