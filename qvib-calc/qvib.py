import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

temp = []
temp = np.linspace(300,2000,18)

file_name = []
for file in os.listdir('./dat'):
    file_name.append(os.path.splitext(file)[0])
print (file_name)

#df.iloc[i]

kb = 1.381e-23
h = 6.62607015e-34
c = 3e10

for f_i in range(0, len(file_name)):
    v_freq = pd.read_csv('./dat/%s.dat'%file_name[f_i], header=None, engine='python')
    f_out = open('%s.out'%file_name[f_i], 'w')
    for T_i in range(0, len(temp)):
        T =temp[T_i]
        qvib = 1
        for i in range(0, len(v_freq)):
            qvib = qvib * 1/(1-np.exp(-h*c*v_freq.iloc[i,0]/kb/T))
            #print (v_freq.iloc[i,0])
            #print (qvib)
        #print (qvib)
        f_out.write ('%d\t%f\n'%(T,qvib))
    f_out.close()

