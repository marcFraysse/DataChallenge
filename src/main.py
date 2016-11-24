import pandas as pd
import numpy as np

data_size = 100;

data = pd.read_csv('../train_2011_2012_2013.csv', parse_dates = ['DATE'], nrows = data_size, sep = ';', usecols=['DATE','DAY_OFF', 'WEEK_END', 'DAY_WE_DS', 'ASS_ASSIGNMENT', 'CSPL_CALLS']) # low_memory=False

pd.set_option('display.max_rows', len(data.iloc[0]))
for i in range(len(data.index)) :
    if data.iloc[i]['CSPL_CALLS'] > 0 : 
        print(data.iloc[i])
        break;
pd.reset_option('display.max_rows')
