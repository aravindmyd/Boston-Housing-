import pandas as pd
import yaml
import subprocess


def set_credentials_on_environment(credential_path: str) -> bool:
    import os
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
    return True


def convert_data_to_df(data, columns) -> pd.DataFrame:
    dic = {}
    for i in range(len(data)):
        dic[columns[i]] = [data[i]]
    df = pd.DataFrame(dic)
    return df


def load_config(property_name: str = None, config_file_name: str = 'conf.yml'):
    with open(config_file_name, "r") as yml_file:
        cfg = yaml.safe_load(yml_file)

    conf_dic = cfg["table"]
    if property_name:
        if property_name in conf_dic.keys(): return conf_dic[property_name]
    return conf_dic


# print(load_config(property_name='default_values'))

def get_binary_from_gs_bucket(gs_file_path: str = 'boston_housing_pred/output',
                              binary_file_name: str = 'boston_model_binary'):
    cmd = f'gsutil cp gs://{gs_file_path}/{binary_file_name} .'
    print(subprocess.getoutput(cmd))
    return True


set_credentials_on_environment("/Users/av/PycharmProjects/Boston-Home-Prediction/key.json")
#print(get_binary_from_gs_bucket())
