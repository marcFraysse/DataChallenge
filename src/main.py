import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import time
import datetime

from sklearn.tree import DecisionTreeRegressor

data_size = -1; #max is 1030829
resFileName = '../submissionQ95.txt'
showGraphs= False;

reg = DecisionTreeRegressor(max_depth=2)

start_time = time.time()

def computePrediction(date, assignment, data):
    weekend = (date.weekday() > 4)
    relevant = data.loc[lambda x : 
                        (x.WEEK_END == weekend) & 
                        (x.ASS_ASSIGNMENT == assignment) & 
                        (x.HOUR == date.hour) & 
                        (x.DATE < date + datetime.timedelta(30)) &
                        (x.DATE > date - datetime.timedelta(30))]
    if len(relevant) > 0 :
        if showGraphs and relevant.quantile(0.95).CSPL_CALLS > 0 :
            relevant.CSPL_CALLS.plot(marker='o')
            print(str(len(relevant)) + " points plotted, result is : " + str(relevant.quantile(0.95, interpolation='higher').CSPL_CALLS))
            plt.show()
            plt.close()
        return relevant.quantile(0.95, interpolation='higher').CSPL_CALLS
    else :
        return 0
    
def computeTimeString():
    t = time.time() - start_time
    if t < 60 :
        return "%.2f" % (time.time() - start_time) + " sec."
    else : 
        return str(int(t/60)) + " min " + str(int(t % 60)) + " sec."
    
def loadData() : 
    if data_size > 0 : 
        data = pd.read_csv('../train_2011_2012_2013.csv', nrows = data_size, parse_dates = ['DATE'], sep = ';',  engine='c', usecols=['DATE','DAY_OFF', 'WEEK_END', 'DAY_WE_DS', 'ASS_ASSIGNMENT', 'CSPL_CALLS']) # low_memory=False
    else : 
        data = pd.read_csv('../train_2011_2012_2013.csv', parse_dates = ['DATE'], sep = ';',  engine='c', usecols=['DATE','DAY_OFF', 'WEEK_END', 'DAY_WE_DS', 'ASS_ASSIGNMENT', 'CSPL_CALLS']) # low_memory=False

    data['DATE'] = pd.to_datetime(data['DATE'], unit='ms')

    pd.set_option('display.max_rows', len(data.iloc[0]))
    data = data.groupby(['DATE', 'ASS_ASSIGNMENT', 'WEEK_END']).sum().reset_index()
    data['WEEKDAY'] = data['DATE'].map(lambda x : x.weekday())
    data['MONTH'] = data['DATE'].map(lambda x : x.month)
    data['HOUR'] = data['DATE'].map(lambda x : x.hour)
    data['MINUTE'] = data['DATE'].map(lambda x : x.minute)
    return data

def loadPredictions() : 
    prediction = pd.read_table('../submission.txt', parse_dates = ['DATE'])
    return prediction

###########################################
################### CODE ##################
###########################################

data = loadData();
prediction = loadPredictions()
print("Training data is loaded (" + str(len(data.index)) + ")")

nonZeroRes = 0;
predictionsNb = len(prediction.index)
computed = {}

for i in range(predictionsNb) :
    if (i % 100 == 0) :
        print("Dealing with test case " + str(i) + "/" + str(predictionsNb) + " \t(" + "%.2f" % (100*i/predictionsNb) + "% in " + computeTimeString() + " )")
    date = prediction.iloc[i]['DATE']
    assignment = prediction.iloc[i]['ASS_ASSIGNMENT']
    if (date, assignment) in computed :
        res = computed[(date, assignment)]
    else :
        res = computePrediction(date, assignment, data)
        if res > 0 : 
            nonZeroRes += 1
        computed[(date, assignment)] = res
    prediction.set_value(i,'prediction',res)
    
print("Computation finished. Non zero value computed : " + str(nonZeroRes))

prediction.to_csv(resFileName, sep = '\t', index = False, encoding ='utf-8')
print("Saved to " + resFileName)
pd.reset_option('display.max_rows')


