import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shutil 
import os


if os.path.exists('./__outputs__') == 0:
    os.makedirs ('./__outputs__')

df = pd.read_csv('./irc_files/energy.dat',sep='\t\t', header=None, engine='python')
df_2= pd.read_csv('./__inputs__/energy_barrier.inp',engine='python')
ts_ene = df_2.iloc[0,0]
##读取energy表格数据，没有列名称，以双制表符分割 以空格分列：delim_whitespace = True

#过渡态能量HF
init_ene = df.iloc[0,1] ## 0行1列 （第一行第二列） 

#df_out = pd.DataFrame(data=[],columns = ('Energy (kcal/mol)'))

irc_ene_hf = []
irc_ene_kcal = []

for i in range (len(df)):
    irc_ene_hf.append (df.iloc [i,1])  ##向数组中添加元素
    
#print (irc_ene_hf)

for i in range(len(irc_ene_hf)):
    irc_ene_kcal.append(627.5*(irc_ene_hf[i] - init_ene))
    
#print (irc_ene_kcal)

f_out = open('./__outputs__/energy_out_kcal.out', 'w')

irc_ene_kcal_corr = 0
for x in range(len(irc_ene_kcal)):
    irc_ene_kcal_corr = irc_ene_kcal[x] + ts_ene
    f_out.write ('E%d\t\t%s\n'%(x,irc_ene_kcal_corr))
    print (irc_ene_kcal_corr)

'''
    # 使用DataFrame 和 iloc 进行单行/列的选择
    # 行选择：
    data.iloc[0] # 数据中的第一行
    data.iloc[1] # 数据中的第二行
    data.iloc[-1] # 数据中的最后一行
    
    # 列选择：
    data.iloc[:, 0] # 数据中的第一列
    data.iloc[:, 1] # 数据中的第二列
    data.iloc[:, -1] # 数据中的最后一列 
————————————————
版权声明：本文为CSDN博主「&quot;灼灼其华&quot;」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/weixin_44285715/article/details/100116192
'''
    
