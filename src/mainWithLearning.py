import pandas as pd 
import numpy as np
import time
import datetime
import json

resFileName = '../submissionQ95.txt'

def loadPredictions() : 
    prediction = pd.read_table('../submission.txt', parse_dates = ['DATE'])
    return prediction

def hashCode(day,year, month, hour, ass_assignment):
    hash = str(day//5) +str(year) + str(month) + str(hour) + ass_assignment
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
        if(hashCode(date.weekday(),date.year,date.month,date.hour,assignment) in quantiles):
            res = quantiles[hashCode(date.weekday(),date.year,date.month,date.hour,assignment)]
            if res>100:
                res += 25
            elif res>40:
                res -= 6
            elif res >7:
                res -= 8
        else:
            res = 0
        if res > 0 : 
            nonZeroRes += 1
        computed[(date, assignment)] = res
    prediction.set_value(i,'prediction',res)
    
print("Computation finished. Non zero value computed : " + str(nonZeroRes))

prediction.to_csv(resFileName, sep = '\t', index = False, encoding ='utf-8')
print("Saved to " + resFileName)
pd.reset_option('display.max_rows')