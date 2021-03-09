import sys
import linecache
import pandas as pd
import re
import os
import shutil 
import time

if os.path.exists('./mess_files') == 0:
    os.makedirs ('./mess_files')

irc_steps_read = pd.read_csv('./irc_files/irc_steps.rwf', header=None, engine='python')
irc_steps = irc_steps_read.iloc[0,0]
print ('irc steps: %d'%irc_steps)

mess_out = open('./__outputs__/mess_vtst.inp', 'w')
mess_out.write (' Barrier      B1 R1 W1\n')
mess_out.write ('  Variational\n')

for steps_vtst in range(0,irc_steps):
	geo_inp = pd.read_csv ('./irc_files/geo_%d.dat'%steps_vtst,delim_whitespace = True,header = None, skiprows = 1, engine = 'python')
	#geo_inp = pd.read_csv ('./irc_files/geo_0.dat',delim_whitespace = True,header = None, skiprows = 1, engine = 'python')
	#print(geo_inp)
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
rows_geo = 0

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


ess_inp = pd.read_csv ('./__inputs__/mess_ess.dat',delim_whitespace = True,header = None, engine = 'python')
sym_fact = ess_inp.iloc[0,1]
welldepth_1 = ess_inp.iloc[1,1]
welldepth_2 = ess_inp.iloc[2,1]
#####筛选频率
for steps_vtst in range(0,irc_steps):
    freq_temp = pd.read_csv ('./irc_files/RPHt_%d/hrproj_freq.dat'%steps_vtst, delim_whitespace = True,header = None, engine = 'python')
    freq_clean = pd.DataFrame (data=[])
    for i in range (0,freq_temp.shape[0]):
        if freq_temp.iloc [i,0] > 0.0:
            freq_clean = freq_clean.append (freq_temp.iloc[i])
        freq_clean.to_csv ('./mess_files/freq_temp_%d'%steps_vtst, float_format='%.2f', index=False, header = False,)

if os.path.exists('./mess_files/debug') == 0:
    os.makedirs ('./mess_files/debug')

for steps_vtst in range(0,irc_steps):
    freq_temp = pd.read_csv ('./irc_files/RPHt_%d/hrproj_freq.dat'%steps_vtst, delim_whitespace = True,header = None, engine = 'python')
    freq_clean = pd.DataFrame (data=[])
    for i in range (0,freq_temp.shape[0]):
        if freq_temp.iloc [i,0] != 0.0:
            freq_clean = freq_clean.append (freq_temp.iloc[i])
        freq_clean.to_csv ('./mess_files/debug/freq_debug_%d'%steps_vtst, float_format='%.2f', index=False, header = False,)
###################
time.sleep(5)

freq_0_parse = pd.read_csv ('./mess_files/freq_temp_0', header = None, engine = 'python')
freqs = freq_0_parse.shape[0]

img_freq_parse = pd.read_csv ('./mess_files/debug/freq_debug_0', header = None, engine = 'python')
img_freq_0 = img_freq_parse.iloc[-1,0]
img_freq = (-1) *  img_freq_0
#################zpe
energy_frame = pd.read_csv ('./__outputs__/energy_out_kcal.out',sep = '\t\t', header=None, engine='python')
zpe = []
for i in range (0,energy_frame.shape[0]):
    zpe.append(energy_frame.iloc[i,1])

#################zpe

for i in range(0,irc_steps):
    mess_out.write ('   RRHO    !%d\n'%(i+1))
    mess_out.write ('Geometry[angstrom]         %d\n'%rows_geo)
    geo_readln = open('./mess_files/geo_temp2_%d'%i, 'r')
    for lines in geo_readln.readlines():
        mess_out.write (lines)
    geo_readln.close()
    #mess_out.write ('\n')
    mess_out.write ('   Core 	RigidRotor\n')
    mess_out.write ('       SymmetryFactor      %.2f\n'%sym_fact)
    mess_out.write ('   End\n')
    rotor_inp = open ('./__inputs__/mess_rotors.dat', 'r')
    for lines in rotor_inp.readlines():
        mess_out.write (lines)
    mess_out.write ('   Frequencies[1/cm]      %d\n'%freqs)
    rotor_inp.close()
    freq_count_read = open ('./mess_files/freq_temp_%d'%i, 'r')
    freq_counter = 0
    for lines in freq_count_read.readlines():
        freq_counter += 1
    freq_count_read.close()
    if freq_counter < freqs:
        freq_inp_debug = open ('./mess_files/debug/freq_debug_%d'%i, 'r')
        for lines in freq_inp_debug.readlines():
            mess_out.write(lines)
        mess_out.write('!!!!!!!!!warning!!!  two img freqs found!!!!!!!!!\n\n')
        freq_inp_debug.close()
    else:
        freq_inp = open ('./mess_files/freq_temp_%d'%i, 'r')
        for lines in freq_inp.readlines():
            mess_out.write(lines)
        freq_inp.close()
    mess_out.write (' ZeroEnergy[kcal/mol]    %.5f\n'%zpe[i])
    mess_out.write (' ElectronicLevels[1/cm]                      1\n')
    mess_out.write (' 0.0000000000000000        2.0000000000000000\n')
    mess_out.write ('End\n')
    mess_out.write ('!***************************************!\n')

mess_out.write ('   Tunneling    Eckart\n')
mess_out.write ('   ImaginaryFrequency[1/cm]        %.2f\n'%img_freq)
mess_out.write ('   WellDepth[kcal/mol]     %.1f\n'%welldepth_1)
mess_out.write ('   WellDepth[kcal/mol]     %.1f\n'%welldepth_2)
mess_out.write ('End\n')
mess_out.write ('End\n')
mess_out.write ('End\n')
mess_out.close()
