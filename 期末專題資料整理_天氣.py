# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 13:55:45 2022

@author: Shuo-Yang
"""

import pandas as pd
import os, sys
import re
import numpy as np

#1. 將25年氣象資料依照各年分合併
for i in range(1997,2023):
    path = f'./{i}'
    dir = os.listdir(path)
    if dir[0]=='desktop.ini':
        dir.remove("desktop.ini")
    df=pd.DataFrame()
    for d in dir : 
        data = pd.read_csv(f'{path}/{d}').iloc[1:,:]
        data.insert(1,"country",d.split('-')[0])
        #data.insert(2,"location",d.split('-')[1])
        data.insert(0,"year",d.split('-')[3])
        data.insert(1,"month",d.split('-')[4].split('.')[0])
        df = pd.concat([df,data])
    df.to_csv(f'{i}.csv')
    
#2. 合併25年氣象資料
df=pd.DataFrame()
for i in range(1997,2023):
    data=pd.read_csv(f'{i}.csv')
    df = pd.concat([df,data])
df.reset_index(drop=True)
df.to_csv('allweather1.csv')

#3. 取代特殊符號
df.replace({
    '...':None,
    'T':'0.05',
    '/':None,
    'X':None,
    '&':None},inplace=True)
#4. 加入日期欄位
df.iloc[:,[0,1,2]]=df.iloc[:,[0,1,2]].astype(str)
df.insert(3,"date",df[['year', 'month','觀測時間(day)']].apply('-'.join, axis=1))

#5. 橫向刪除空值
df.dropna(thresh=6,axis=0,inplace = True)

#6. 縱向刪除空值
mask=(df.isnull().sum()/len(df.index))<0.8
df2=df.loc[:,mask]



