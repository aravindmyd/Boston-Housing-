from utils import get_table_as_df,save_binary_to_gsbucket
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import datalab.storage as gcs
import logging as log
log.basicConfig(level=log.CRITICAL)

def store_test_data_gcs(X_test,Y_test,bucket_name : str = "boston_housing_pred") -> bool:
    gcs.Bucket(bucket_name).item('output/X_test.csv').write_to(X_test.to_csv(),'text/csv')
    gcs.Bucket(bucket_name).item('output/Y_test.csv').write_to(Y_test.to_csv(),'text/csv')
    return True


def init(table_name : str = 'fe_table') -> bool:
    preprocessed_df = get_table_as_df(table_name = table_name)
    
    #Model Training
    
    #Splitting the data and target
    log.info("Splitting the data and target")
    X = preprocessed_df.drop(['price'], axis=1)
    Y = preprocessed_df['price']
    
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state = 2)
    log.info(f"X-Shape:{X.shape}\nX-Train Shape:{X_train.shape}\nX-TestShape:{ X_test.shape}")
    y = np.round(preprocessed_df['price'])
    model = ExtraTreesClassifier()
    model.fit(X,y)
    
    X = preprocessed_df.iloc[:,[-1,5,10,4,9]] # Based on SelectKBest class
    y = preprocessed_df.iloc[:,[-1]]
    

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=0)
    reg = RandomForestRegressor()
    reg.fit(X_train,y_train)
    
    y_pred = reg.predict(X_test)
    
    log.info("Saving model Binary")
    log.info(f"Testing Accuracy: {reg.score(X_test,y_test)*100}")
    save_binary_to_gsbucket(model,"boston_housing_pred","boston_model_binary")
    log.info(f"Model Binary Saved")
    
    log.info("Storing test rows to gcs")
    store_test_data_gcs(X_test,Y_test)

    return True


    
init()
