# -*- coding: utf-8 -*-
"""
Created on Sun Oct  2 16:39:52 2022

@author: 88693
"""

import pandas as pd
import os, sys
import re
import numpy as np

price = pd.read_csv('allprice.csv',index_col=0)
price = price[price['Unnamed: 1'].notnull()]
price = price[price.iloc[:,1].str.contains('台北一')]

price.rename(columns={'蔬菜 產品日交易行情': 'date','Unnamed: 6': 'price','Unnamed: 8': 'volume'}, inplace=True)
price=price.iloc[:,[0,6,8]]
price.sort_values(by='date',inplace=True)
price.reset_index(inplace=True,drop=True)

price.to_csv('price.csv')