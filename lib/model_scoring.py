import gcsfs
import pickle
from utils import convert_data_to_df
import logging as log
log.basicConfig(level=log.INFO)


def init(gs_file_path : str = 'boston_housing_pred/output',binary_file_name : str = 'boston_model_binary'):
    fs = gcsfs.GCSFileSystem()
    binary_file_path = f'gs://{gs_file_path}/{binary_file_name}'
    #binary_file_path = 'boston_housing_pred/output/boston_model_binary'
    with fs.open(binary_file_path,'rb') as file:
        model = pickle.load(file) 
    
    test = [ 0.00632,18.0,2.31,0,0.538,6.575,65.2,4.0900,1,296,15.3,396.90,4.98]
    columns = ['crim',
     'zn',
     'indus',
     'chas',
     'nox',
     'rm',
     'age',
     'dis',
     'rad',
     'tax',
     'ptratio',
     'b',
     'lstat']
    df = convert_data_to_df(test,columns)
    score = model.predict(df)
    return score[0]

print(init())