import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

filename = 'timhis_JSR_1075'
##分析cantera输出的timehistory数据

df = pd.read_csv('%s.dat'%filename,engine='python')
df_r = pd.DataFrame(data=[],columns = [('X_O2')])

d1 = df['O2']
df_r['X_O2'] = d1
print(df_r)
df_r.to_csv('%s_sorted.csv'%filename)
