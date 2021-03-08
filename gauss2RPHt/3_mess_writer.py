import sys
import linecache
import pandas as pd
import re
import os

os.makedirs ('./mess_files')

irc_steps_read = pd.read_csv('./irc_files/irc_steps.rwf', header=None, engine='python')
irc_steps = irc_steps_read.iloc[0,0]
print (irc_steps)

mess_out = open('./mess_files/mess_vtst.inp', 'w')
mess_out.write (' Barrier      B1 R1 W1')
mess_out.write ('  Variational')

for steps_vtst in range(0,irc_steps):
	geo_inp = pd.read_csv ('./irc_files/geo_%d.dat'%steps_vtst,delim_whitespace = True,header = None, skiprows = 1, engine = 'python')
	#geo_inp = pd.read_csv ('./irc_files/geo_0.dat',delim_whitespace = True,header = None, skiprows = 1, engine = 'python')
	print(geo_inp)
	geo_temp1 = pd.DataFrame(data=[], columns = ('a','b','c','d'))
	geo_temp1['a'] = geo_inp.iloc[:,1]
	geo_temp1['b'] = geo_inp.iloc[:,3]
	geo_temp1['c'] = geo_inp.iloc[:,4]
	geo_temp1['d'] = geo_inp.iloc[:,5]
	#geo_temp1 = geo_temp1.round(2)
	geo_temp1.to_csv ('./mess_files/geo_temp1_%d'%steps_vtst,float_format='%.6f', index=False, header = False, sep = '\t')
	#替换第二列 元素符号
'''
返回列数：

df.shape[1]

返回行数：

df.shape[0]
'''

for steps_vtst in range(0,irc_steps):
    geo_temp2 = pd.read_csv ('./mess_files/geo_temp1_%d'%steps_vtst,delim_whitespace = True,header = None, engine = 'python')
    rows_geo = geo_temp2.shape[0]
    for i in range (0, rows_geo):
        if geo_temp2.iloc[i,0] == 1:
            geo_temp2.iloc[i,0] = 'H'
        elif geo_temp2.iloc[i,0] == 6:
            geo_temp2.iloc[i,0] = 'C'
        else:
            geo_temp2.iloc[i,0] = 'O'
    geo_temp2.to_csv ('./mess_files/geo_temp2_%d'%steps_vtst,float_format='%.6f', index=False, header = False, sep = '\t')
        
