from promptflow import tool
import pandas as pd
from controllers.bigquery import get_dataset_metadata, exe_query
# from utils.logger import logger


@tool
def get_table_info(dataset_id:str):
    # toodo:外して、envファイルを変更する
    # toodo:headでデータのサンプルも追加する
    dataset_id = 'eparkdb.restaurants_kaggle'
    dataset_schemas = get_dataset_metadata(dataset_id)
    table_info = str(dataset_schemas)
    return table_info


# def get_table_info(dataset_id:str, table_id:str):
#     dataset = get_dataset_metadata(dataset_id)
#     table = dataset.get_table_by_id(table_id)
#     schema = str(table)

#     query = f'SELECT * FROM {dataset_id}.{table_id} LIMIT 3'
#     df = exe_query(query)
#     sample_data = df.to_string()
#     table_info = schema + ";\nsample:" + query + "\n" + sample_data

#     return table_info
