from promptflow import tool
import pandas as pd
from controllers.bigquery import get_dataset_metadata, exe_query
# from utils.logger import logger


# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need

@tool
def get_table_info(dataset_id:str, table_id:str):
    dataset = get_dataset_metadata(dataset_id)
    table = dataset.get_table_by_id(table_id)
    schema = str(table)

    query = f'SELECT * FROM {dataset_id}.{table_id} LIMIT 3'
    df = exe_query(query)
    sample_data = df.to_string()
    table_info = schema + ";\nsample:" + query + "\n" + sample_data

    return table_info
