# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 13:19:02 2022

@author: Student
"""
import pandas as pd
from datetime import timedelta,datetime

tp = pd.read_excel('19952022.xlsx')

# 1.刪除不需要的欄位 
tp.drop(columns=['年份','颱風名稱'],axis=1,inplace=True)

# 2.切分時間為颱風起訖
tp_time = tp.iloc[:,2]

tp_start = tp_time[::2]
tp_start.reset_index(inplace = True , drop = True)

tp_end = tp_time[1::2]
tp_end.reset_index(inplace = True , drop = True)

tp_time = pd.concat([tp_start,tp_end],axis = 1)

tp_time.columns = ['start','end']

# 3. 合併且重新命名

tp.drop(['警報期間'],axis = 1,inplace=True)

tp=tp.iloc[::2,:]

tp.reset_index(inplace=True,drop=True)

final = pd.concat([tp_time,tp],axis = 1)

final.columns = ['start','end','typhoon_number','path','level','minimum_pressure','maximum_windspeed','storm_radius7','storm_radius10','alarms_count']

# 4. 建立時間序列資料
final['end']=final['end']+timedelta(days=1)
typhoon = pd.concat([pd.DataFrame({
               'date': pd.date_range(row.start, row.end, freq='D'),
               'typhoon_number': row.typhoon_number,
               'path': row.path,
               'level': row.level,            
               'minimum_pressure':row.minimum_pressure,
               'maximum_windspeed':row.maximum_windspeed,
               'storm_radius7':row.storm_radius7,
               'storm_radius10':row.storm_radius10,
               'alarms_count':row.alarms_count
                           }, columns=['date','typhoon_number','path','level','minimum_pressure','maximum_windspeed','storm_radius7','storm_radius10','alarms_count']) 
           for i, row in final.iterrows()], ignore_index=True)

# 5.匯出檔案
typhoon.to_csv('typhoon.csv')