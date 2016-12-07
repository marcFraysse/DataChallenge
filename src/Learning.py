import pandas as pd 
import numpy as np
import time
import datetime
import json


data_size = -1; #max is 1030829
resFileName = '../submissionQ95.txt'
showGraphs= False;


start_time = time.time()

def loadData() : 
    if data_size > 0 : 
        data = pd.read_csv('../train_2011_2012_2013.csv', nrows = data_size, parse_dates = ['DATE'], sep = ';',  engine='c', usecols=['DATE','DAY_OFF', 'WEEK_END', 'DAY_WE_DS', 'ASS_ASSIGNMENT', 'CSPL_RECEIVED_CALLS']) # low_memory=False
    else : 
        data = pd.read_csv('../train_2011_2012_2013.csv', parse_dates = ['DATE'], sep = ';',  engine='c', usecols=['DATE','DAY_OFF', 'WEEK_END', 'DAY_WE_DS', 'ASS_ASSIGNMENT', 'CSPL_RECEIVED_CALLS']) # low_memory=False

    data['DATE'] = pd.to_datetime(data['DATE'], unit='ms')

    pd.set_option('display.max_rows', len(data.iloc[0]))
    data = data.groupby(['DATE', 'ASS_ASSIGNMENT', 'WEEK_END']).sum().reset_index()
    data['WEEKDAY'] = data['DATE'].map(lambda x : x.weekday())
    data['MONTH'] = data['DATE'].map(lambda x : x.month)
    data['HOUR'] = data['DATE'].map(lambda x : x.hour)
    data['MINUTE'] = data['DATE'].map(lambda x : x.minute)
    return data

def hashCode(weekday,year, month, hour, ass_assignment):
    hash = str(weekday//5) +str(year) + str(month) + str(hour) + ass_assignment
    return hash

""" Main frame """

data = loadData();
relevant = {}
quantiles = {}

dataNb = len(data.index)

for i in range(dataNb):
    date = data.iloc[i]['DATE']
    assignment = data.iloc[i]['ASS_ASSIGNMENT']
    if(not hashCode(date.weekday(),date.year,date.month,date.hour,assignment) in relevant):
        relevant[hashCode(date.weekday(),date.year,date.month,date.hour,assignment)] = np.array([])
    relevant[hashCode(date.weekday(),date.year,date.month,date.hour,assignment)] = np.append(data.iloc[i]['CSPL_RECEIVED_CALLS'],relevant[hashCode(date.weekday(),date.year,date.month,date.hour,assignment)])
    if(i%10000==0):    
        print(i)
for key in relevant.keys():
    quantiles[key] = np.percentile(relevant[key],95)


with open('learning.json', 'w') as outfile:
    json.dump(quantiles, outfile)
outfile.close()







