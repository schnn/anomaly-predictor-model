########################################################### {COPYRIGHT-TOP} ####
# Licensed Materials - Property of IBM
# 5900-AEO
#
# Copyright IBM Corp. 2020. All Rights Reserved.
#
# US Government Users Restricted Rights - Use, duplication, or
# disclosure restricted by GSA ADP Schedule Contract with IBM Corp.
########################################################### {COPYRIGHT-END} ####
def train_model():

    import os
    import sys
    assert sys.version_info >= (3, 5)
    
    import pandas as pd
    import seaborn as sns 
    from datetime import datetime
    import numpy as np
    from sklearn.neighbors import NearestNeighbors
    from kneebow.rotor import Rotor
    import pickle
    sns.set(style="darkgrid")

    from pathlib import Path

    import datetime as dt

    DATA_OUT_DIR = os.environ['DATA_OUT_DIR']
    DATA_OUT_NAME = os.environ['DATA_OUT_NAME']
    MODEL_DIR = os.environ['MODEL_DIR']
    MODEL_FILE_NAME = os.environ['DATA_FILE_NAME']
    DF_COLS =(os.environ['DF_COLS']).split(",")

    print(DF_COLS)
    dfObj = pd.DataFrame(columns = DF_COLS) 
    print(dfObj)

    print("print dataframe read from mounted location")
    print(os.listdir(DATA_OUT_DIR))
    
    
    # Calculating the EPS values that is needed for the models

    dfObj = pd.read_csv(os.path.join(DATA_OUT_DIR, DATA_OUT_NAME), sep=',', names=DF_COLS)
    print(dfObj.columns.values)
    print(dfObj)
    # data = pd.read_csv('clean_data.csv')

    # Finding the unique process Id in the dataset
    uniquePIDs = dfObj["ProcessId"].unique()

    print('There are',uniquePIDs.size,'process runs in the dataset \n')

    tot={}
    pids = []
    steps = []
    time = []

    for Pids in uniquePIDs:

        # print(Pids)
        dataByPid = dfObj.loc[dfObj["ProcessId"] == Pids]
        dataByPid.sort_values(by="Start_date", inplace=True)

        # print(dataByPid)
        processStartTime = pd.to_datetime(dataByPid.iloc[0]["Start_date"])
        processEndTime = pd.to_datetime(dataByPid.iloc[len(dataByPid)-1]["End_date"])
        
        # print(Pids,"->",processStartTime,"-",processEndTime)
        # print("Turn around time for Process",Pids,"is",processEndTime-processStartTime)
        tot[Pids]=(processEndTime-processStartTime).total_seconds()
        pids.append(Pids)
        steps.append(len(dataByPid)-1)
        time.append((processEndTime-processStartTime).total_seconds())

    finalData = pd.DataFrame({'ProcessId':pids,'ActivityCount':steps,'Time':time})

    # Calculating the optimal EPS

    superFinalData = finalData[["ActivityCount","Time"]]

    # print(superFinalData)
    neigh = NearestNeighbors(n_neighbors=2)
    nbrs = neigh.fit(superFinalData)
    distances, indices = nbrs.kneighbors(superFinalData)
    # print(distances)
    rotor = Rotor()
    rotor.fit_rotate(distances)
    elbow_index = rotor.get_elbow_index()

    print("EPS value")
    print(int(distances[elbow_index][1]))
    EPS_VALUE = int(distances[elbow_index][1])


    # Calculating the typical times for each activity

    # Finding the unique process Id in the dataset
    uniqueActivities = dfObj["ActivityName"].unique()

    AvgActivityTimes = {}

    def findAvgTime(activities):
        activityTimes = []
        for index,acti in activities.iterrows():
            activityTimes.append((pd.to_datetime(acti["End_date"]) - pd.to_datetime(acti["Start_date"])).total_seconds())
        # print(int(np.mean(activityTimes)))
        return int(np.mean(activityTimes))

    for activity in uniqueActivities:
        acti = dfObj.loc[dfObj["ActivityName"] == activity]
        AvgActivityTimes[activity] = findAvgTime(acti)

    print(AvgActivityTimes)

    ### Save model

    # Create directories if not exists
    print("print model saved to location")
    Path(MODEL_DIR).mkdir(parents=True, exist_ok=True)
    
    model_location=os.path.join(MODEL_DIR,MODEL_FILE_NAME)
    print(model_location)

    with open(model_location, 'wb') as handle:
        pickle.dump({"eps":EPS_VALUE,"min_values":4,"AvgActivityTimes":AvgActivityTimes}, handle, protocol=pickle.HIGHEST_PROTOCOL)

    #model.save(model_location)
    #pickle.dump(model, open(filename, 'wb'))
    print("print mounted location post saving model")
    print(os.listdir(MODEL_DIR))



if __name__ == "__main__":
    train_model()
        
