from pandas import DataFrame
from lib.utils import save_df_to_bq, get_table_as_df
import logging as log

log.basicConfig(level=log.INFO)


def init(project_id: str = "axial-iris-354312", dataset_name: str = "boston_housing_dataset",
         write_table_name: str = 'fe_table') -> DataFrame:
    boston_df = get_table_as_df()
    boston_df.dropna()
    boston_df.rename(columns={'medv': 'price'}, inplace=True)
    log.info(f"Updating preprocessed df to {write_table_name} bq table.....")
    save_df_to_bq(boston_df, project_id, dataset_name, write_table_name)
    log.info(f"Preprocess Done!")
    return boston_df


log.info(f"Sample Loaded data \n {init().head(5)}")
