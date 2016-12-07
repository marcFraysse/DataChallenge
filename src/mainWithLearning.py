import pandas as pd 
import numpy as np
import time
import datetime
import json

resFileName = '../submissionQ95.txt'

def loadPredictions() : 
    prediction = pd.read_table('../submission.txt', parse_dates = ['DATE'])
    return prediction

def hashCode(weekday, month, hour, ass_assignment):
    hash = str(weekday//5) + str(month) + str(hour) + ass_assignment
    return hash

""" main frame """

prediction = loadPredictions()

nonZeroRes = 0;
predictionsNb = len(prediction.index)
computed = {}


"""load json here """

with open("learning.json") as learning:
    quantiles = json.load(learning)

for i in range(predictionsNb) :
    date = prediction.iloc[i]['DATE']
    assignment = prediction.iloc[i]['ASS_ASSIGNMENT']
    if (date, assignment) in computed :
        res = computed[(date, assignment)]
    else :
        if(hashCode(date.weekday(),date.month,date.hour,assignment) in quantiles):
            res = quantiles[hashCode(date.weekday(),date.month,date.hour,assignment)]
        else:
            res = 10
        if res > 0 : 
            nonZeroRes += 1
        computed[(date, assignment)] = res
    prediction.set_value(i,'prediction',res)
    
print("Computation finished. Non zero value computed : " + str(nonZeroRes))

prediction.to_csv(resFileName, sep = '\t', index = False, encoding ='utf-8')
print("Saved to " + resFileName)
pd.reset_option('display.max_rows')