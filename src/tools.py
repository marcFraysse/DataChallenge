import pandas as pd 


data_size = -1; #max is 1030829
resFileName = '../submissionQ95.txt'
showGraphs= False;


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

def hashCode(day,year, month, hour, ass_assignment):
    hash = str(day//5) +str(year) + str(month) + str(hour) + ass_assignment
    return hash

def loadPredictions() : 
    prediction = pd.read_table('../submission.txt', parse_dates = ['DATE'])
    return prediction