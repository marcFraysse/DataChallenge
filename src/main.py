import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
 
from sklearn import linear_model

#data_size = 1030829; #max is 1030829
resFileName = '../submission001.txt'

reg = linear_model.LinearRegression()

def computePrediction(date, assignment, data):
    relevant = data.loc[lambda x : (x.WEEKDAY == date.weekday()) & (x.ASS_ASSIGNMENT == assignment) & (x.HOUR == date.hour)]
    if len(relevant) > 0 :
#         if relevant.quantile(0.9).CSPL_CALLS > 0 :
#             print(len(relevant)) 
#             relevant.plot(['DATE'],['CSPL_CALLS'], marker='o')
#             plt.show()
#             plt.close()
        return relevant.quantile(0.9).CSPL_CALLS
    else :
        return 0
    
def loadData() : 
    #nrows = data_size, 
    data = pd.read_csv('../train_2011_2012_2013.csv', parse_dates = ['DATE'], sep = ';',  engine='c', usecols=['DATE','DAY_OFF', 'WEEK_END', 'DAY_WE_DS', 'ASS_ASSIGNMENT', 'CSPL_CALLS']) # low_memory=False
    data['DATE'] = pd.to_datetime(data['DATE'], unit='ms')
    data['WEEKDAY'] = data['DATE'].map(lambda x : x.weekday());
    data['HOUR'] = data['DATE'].map(lambda x : x.hour);
    data['MINUTE'] = data['DATE'].map(lambda x : x.minute);
    pd.set_option('display.max_rows', len(data.iloc[0]))
    data = data.groupby(['DATE', 'ASS_ASSIGNMENT']).sum().reset_index()
    return data

def loadPredictions() : 
    prediction = pd.read_table('../submission.txt', parse_dates = ['DATE'])
    return prediction

data = loadData();
prediction = loadPredictions()
print("Training data is loaded (" + str(len(data.index)) + ")")

nonZeroRes = 0;

for i in range(len(prediction.index)) :
    if (i % 100 == 0) :
        print("Dealing with test case " + str(i) + "/" + str(len(prediction.index)))
    date = prediction.iloc[i]['DATE']
    assignment = prediction.iloc[i]['ASS_ASSIGNMENT']
    computePrediction(date, assignment, data)
    res = computePrediction(date, assignment, data)
    if res > 0 : 
        nonZeroRes += 1
    prediction.set_value(i,'prediction',res)
    
print("Computation finished. Non zero value computed : " + str(nonZeroRes))

prediction.to_csv(resFileName, sep = '\t', index = False)
print("Saved to " + resFileName)
pd.reset_option('display.max_rows')


