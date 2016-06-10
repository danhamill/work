# -*- coding: utf-8 -*-
"""
Created on Thu Jun 09 16:05:13 2016

@author: dan
"""

import pandas as pd
from glob import glob

files = glob(r'C:\workspace\Reach_4a\Multibeam\xyz\2012_05\*025m.xyz')
def subsetdf(df):
    df = df
    df = df[['x','y','z']]
    return df

data1 = pd.read_csv(files[0], sep = ',',names = ['x','y','z'])
data2 = pd.read_csv(files[1], sep = ',',names = ['x','y','z'])
data3 = pd.read_csv(files[2], sep = ',',names = ['x','y','z'])

data1 = subsetdf(data1)
data2 = subsetdf(data2)
data3 = subsetdf(data3)

frames = [data1,data2,data3]

df = pd.concat(frames)
df.to_csv(r'C:\workspace\Reach_4a\Multibeam\xyz\2012_05\mb_2102_xyz_all_merge.asc', sep=',',index=False)