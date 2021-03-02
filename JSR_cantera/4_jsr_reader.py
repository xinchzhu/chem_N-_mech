import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('jsr_out.out',engine='python')
df_r = pd.DataFrame(data=[],columns = ('Temp','O2'))

d1 = df['Temperature']
d2 = df['O2']
df_r['Temp'] = d1
df_r['O2'] = d2
print(df_r)
df_r.to_csv('jsr_out.csv')


'''
df_r = df_r.append(df.iloc[0]) #按行插入
df_r = df_r.append(df.iloc[:,0]) #按列插入

df_r = df_r.append(df.iloc[i_n])
df_r.to_csv('t3.csv')
'''