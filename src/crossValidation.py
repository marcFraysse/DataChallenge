import json
from src import tools

if __name__=='__main__':

    nonZeroRes = 0;
    data = tools.loadData();

    with open("learning.json") as learning:
        quantiles = json.load(learning)

    for i in range(500000,550000) :
        date = data.iloc[i]['DATE']
        assignment = data.iloc[i]['ASS_ASSIGNMENT']
        if(tools.hashCode(date.weekday(),date.year,date.month,date.hour,assignment) in quantiles):
            res = quantiles[tools.hashCode(date.weekday(),date.year,date.month,date.hour,assignment)]
        else:
            res = 0
        if(abs(data.iloc[i]['CSPL_RECEIVED_CALLS']-res)>10):
            print("real value is " + str(data.iloc[i]['CSPL_RECEIVED_CALLS']) + " and found value is " + str(res))
            
