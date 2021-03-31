########################################################### {COPYRIGHT-TOP} ####
# Licensed Materials - Property of IBM
# 5900-AEO
#
# Copyright IBM Corp. 2020. All Rights Reserved.
#
# US Government Users Restricted Rights - Use, duplication, or
# disclosure restricted by GSA ADP Schedule Contract with IBM Corp.
########################################################### {COPYRIGHT-END} ####
def writeDfToFile(dfObj, dir, fileName) :
    import os

    # saving the dataframe 
    print("print dataframe read from ES saved to location")
    print(os.path.join(dir, fileName))
    dfObj.to_csv(os.path.join(dir, fileName), sep = ',',index=False)

def getDatasets():
    
    import os
    import json
    import pandas as pd

    from pathlib import Path as path
    from elasticsearch import Elasticsearch, exceptions

    ES_SORT = os.environ['ES_SORT']
    ES_URL = os.environ['ES_URL']
    ES_INDEX = os.environ['ES_INDEX']
    ES_QUERY = json.loads(os.environ['ES_QUERY'])
    ES_QRY_PAGE_SIZE = int(os.environ['ES_QRY_PAGE_SIZE'])
    ES_SCROLL_TTL = os.environ['ES_SCROLL_TTL']
    DATA_DIR = os.environ['DATA_DIR']
    DATA_NAME = os.environ['DATA_NAME']
    ES_DATA_FLDS = os.environ['ES_DATA_FLDS'].split(",")
    MAX_RECS_IN_FILE = int(os.environ['MAX_RECS_IN_FILE'])
    PROCESS_ITERATIONS = int(os.environ['PROCESS_ITERATIONS'])

    DF_COLS = ES_DATA_FLDS
    ES_SEARCH_BODY = {
                        "size": ES_QRY_PAGE_SIZE,
                        "query": ES_QUERY,
                     }

    if ( len(ES_SORT) > 0 ) :
        ES_SEARCH_BODY["sort"]  = json.loads(ES_SORT)

    print('**** ES Search ',  ES_SEARCH_BODY)
    

    print("INSIDE GET DATASETS")

    print("print path for shared volume")
    print(DATA_DIR)
    print(DATA_NAME)

    # Create directories if not exists
    path(DATA_DIR).mkdir(parents=True, exist_ok=True)

    # concatenate host string from values
    esClient =  Elasticsearch(ES_URL, 
                                verify_certs=False)

    #Create a DataFrame object
    dfObj = pd.DataFrame(columns = DF_COLS)
    df1 = pd.DataFrame(columns = DF_COLS) 

    print("print dataframe ")
    print(dfObj)

    try:
        # get information on client
        client_info = Elasticsearch.info(esClient)

    except exceptions.ConnectionError as err:
        print ('Elasticsearch client error:', err)
        esClient = None

    if esClient != None:
        resp = esClient.search(
            index = ES_INDEX,
            body = ES_SEARCH_BODY,
            scroll = ES_SCROLL_TTL
        )

    # print(resp)

    frameRow = 0
    fileCounter = 1
    
    # while len(resp['hits']['hits']) and fileCounter <= proc_iter :
    while len(resp['hits']['hits']) :
        print('******  - ', fileCounter, '  ', len(resp['hits']['hits']))

        for x in range (0, len(resp["hits"]["hits"])):
            frameRowData = []
            for fldName in ES_DATA_FLDS:
                frameRowData.append(resp["hits"]["hits"][x]["_source"][fldName])
                #print('***** 1 ', len(resp["hits"]["hits"]), '& ', resp["hits"]["hits"][x]["_source"][fldName])
            dfObj.loc[frameRow] = frameRowData
            # print("printing column")
            # print(dfObj.loc[frameRow]['requestId'])
            frameRow += 1 

        # if frameRow + ES_QRY_PAGE_SIZE > MAX_RECS_IN_FILE :
        if frameRow > MAX_RECS_IN_FILE :
            print("Inside file write IF printing framerow value after writting to file",frameRow)
            currReqId = dfObj.loc[frameRow-1]['requestId']
            print("printing curr reqId")
            print(currReqId)
            df1 = dfObj[dfObj.requestId == currReqId]
            df2 = dfObj[dfObj.requestId != currReqId]
            print("printing next dfObj")
            print(dfObj)
            print("printing next df1")
            print(df1)
            fileName = DATA_NAME.replace(".csv", str(fileCounter) + ".csv") 
            print("wrinting to csv")
            print(df2)
            writeDfToFile(df2, DATA_DIR, fileName)
            dfObj.drop(dfObj.index, inplace=True)
            df2.drop(df2.index, inplace=True)

            if len(df1) > 0 :
                frameRow = len(df1)
                dfObj= df1.copy(deep=True)
                print("printing next dfObj")
                print(dfObj)
                df1.drop(df1.index, inplace=True)
                print("printing df1 after")
                print(df1)
            else :
                frameRow = 0
            
            print("printing framerow value after writting to file",frameRow)
            fileCounter += 1 
            
        scroll_id = resp['_scroll_id']
        resp = esClient.scroll(scroll_id = scroll_id, scroll = ES_SCROLL_TTL)

    esClient.clear_scroll(scroll_id=scroll_id)
    print (dfObj)

    if (frameRow > 0) :
        fileName = DATA_NAME.replace(".csv", str(fileCounter) + ".csv") 
        writeDfToFile(dfObj, DATA_DIR, fileName)

    print(os.listdir(DATA_DIR))
    print(path(os.path.join(DATA_DIR, fileName)).stat().st_size)

if __name__ == "__main__":
    getDatasets()