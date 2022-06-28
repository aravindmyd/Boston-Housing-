from pandas import DataFrame
import pandas as pd
import datalab.storage as gcs
import pickle
import logging as log
log.basicConfig(level=log.INFO)

def set_credentials_on_environment(credential_path: str) -> bool:
    import os
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
    return True
    

def get_table_as_df(project_id: str = "axial-iris-354312", dataset_name: str = "boston_housing_dataset",
                     table_name: str = "boston_housing_table") -> DataFrame:
    from google.cloud import bigquery
    bqclient = bigquery.Client()
    query_string = f"""SELECT * from {project_id}.{dataset_name}.{table_name}"""
    df = (bqclient.query(query_string).result().to_dataframe(create_bqstorage_client=True))
    return df

def save_df_to_bq(df: DataFrame, project_id: str, dataset_name: str, table_name: str,if_exists : str = 'replace') -> bool:
    df.to_gbq(f"{dataset_name}.{table_name}", project_id, if_exists= if_exists)
    log.info(f"Df saved to {table_name} table.")
    return True


def save_binary_to_gsbucket(model_binary, gs_path: str, binary_file_name: str) -> bool:
    gcs.Bucket(gs_path).item(f'output/{binary_file_name}') \
        .write_to(pickle.dumps(model_binary), 'application/octet-stream')
    log.info(f"{binary_file_name} binary saved to {gs_path}")
    return True
    
def convert_data_to_df(data,columns) -> DataFrame:
    dic = {}
    for i in range(len(data)):
        dic[columns[i]] = [data[i]]
    df = pd.DataFrame(dic)
    return df
# data = {'a':[1],'b':[2]}
# df = pd.DataFrame(data)


# save_df_to_bq(df,"axial-iris-354312","boston_housing_dataset",'fe_table')hljlkjl;jljj;jdfl