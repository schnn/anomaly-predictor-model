########################################################### {COPYRIGHT-TOP} ####
# Licensed Materials - Property of IBM
# 5900-AEO
#
# Copyright IBM Corp. 2020. All Rights Reserved.
#
# US Government Users Restricted Rights - Use, duplication, or
# disclosure restricted by GSA ADP Schedule Contract with IBM Corp.
########################################################### {COPYRIGHT-END} ####
def processData():
    
    import os
    import pandas as pd
    import glob
    import numpy as np
    from datetime import datetime

    from pathlib import Path as path
    from numpy import set_printoptions

    print("process Data")

    DATA_DIR = os.environ['DATA_DIR']
    DATA_OUT_DIR = os.environ['DATA_OUT_DIR']
    DATA_OUT_NAME = os.environ['DATA_OUT_NAME']
    DF_COLS =(os.environ['DF_COLS']).split(",")

    print("print dataframe read from mounted location")
    print(os.listdir(DATA_DIR))

    # get data from all the files inside data_dir in loop

    dfObj = pd.DataFrame(columns = DF_COLS) 
    all_files = glob.glob(os.path.join(data_dir, "*"))

    for file in all_files:

        # dfObj = pd.read_csv(file, sep=',', names = ['requestId','activity','dateIn','dateOut'])
        dfObj = pd.read_csv(file, sep=',',usecols=DF_COLS)
        print(file)
        print("Data Read from File")
        print(dfObj)

        # data = pd.read_csv('invenio_tutorial_100tutorial.csv')

        # interestingData = data[["Start_date","End_date","ProcessId","ActivityName"]]
        dfObj["Start_date"] = pd.to_datetime(dfObj["Start_date"],format='%d/%m/%y %H:%M')
        dfObj["End_date"] = pd.to_datetime(dfObj["End_date"],format='%d/%m/%y %H:%M')

        # interestingData.to_csv('clean_data.csv',index=False)

        print(dfObj)

        print(DATA_OUT_DIR)
        path(DATA_OUT_DIR).mkdir(parents=True, exist_ok=True)

        dfObj.to_csv(os.path.join(DATA_OUT_DIR, DATA_OUT_NAME), mode='a',sep = ',',index=False,header=False)
    
        print(os.listdir(DATA_OUT_DIR))
        print(path(os.path.join(DATA_OUT_DIR, DATA_OUT_NAME)).stat().st_size)
        
        # # # df.to_csv('file1.csv')
        # # # saving the dataframe 
        # print("print processed dataframe read from ES and saved to location")
        # print(os.path.join(data_dir, "processed-data.csv"))
        # # # dfSaved = dfSaved.append(df_cat_merge.copy)
        
    # # df.to_csv('file1.csv')
    # # saving the dataframe    
    # dfSaved.to_csv(os.path.join(data_dir, "processed-data.csv"), sep = ',',index=False) 
     
    # print("Data saved to")
    # print(os.listdir(data_dir))
    # # print(path(os.path.join(data_dir, "processed-data.csv")).stat().st_size)
    # print(path(os.path.join(data_dir, "temp-processed-data.csv")).stat().st_size)

if __name__ == "__main__":
    processData()