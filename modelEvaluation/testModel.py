########################################################### {COPYRIGHT-TOP} ####
# Licensed Materials - Property of IBM
# 5900-AEO
#
# Copyright IBM Corp. 2020. All Rights Reserved.
#
# US Government Users Restricted Rights - Use, duplication, or
# disclosure restricted by GSA ADP Schedule Contract with IBM Corp.
########################################################### {COPYRIGHT-END} ####
def test_model():

    import os
    import numpy as np
    import pandas as pd
    import sys
    from pathlib import Path


    ### Restore saved model
    import pickle

    MODEL_DIR = os.environ['MODEL_DIR']
    MODEL_FILE_NAME = os.environ['DATA_FILE_NAME']
    

    print(sklearn.__version__)

    print("print model location")
    model_location=os.path.join(MODEL_DIR,MODEL_FILE_NAME)
    print(model_location)

    # loaded_model = pickle.load(open(model_location, 'rb'))

    with open(model_location, 'rb') as handle:
    hyperParam = pickle.load(handle)
    print(hyperParam)

    # sample = {'dateIn': ['2017-10-02 08:28:09'],'CAT_CODE' : [12] }

    # sample_df = pd.DataFrame(sample, columns = ['dateIn', 'CAT_CODE'])

    # sample_df['dateIn']=sample_df.dateIn.astype('datetime64')
    # sample_df['dateIn']=sample_df['dateIn'].map(dt.datetime.toordinal)

    # sample_pred = loaded_model.predict(sample_df)
    # print(sample_pred)


if __name__ == "__main__":
    test_model()
        
