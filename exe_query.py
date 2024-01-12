from promptflow import tool
from controllers.bigquery import exe_query, upload_dataframe_to_gcs
import json
import pandas as pd
from datetime import datetime


# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(input1: str, input_rfp: str) -> str:
    rfp_dct = json.loads(input1['function_call']['arguments'])
    query = rfp_dct['クエリ']

    try:
        df = exe_query(query)
        bucket_name = 'chat-flow'
        current_time = datetime.now()
        formatted_time = current_time.strftime('%Y%m%d%H%M%S')
        destination_blob_name = f'test/my_data_{formatted_time}.csv'
        public_url = upload_dataframe_to_gcs(df, bucket_name, destination_blob_name)
        print(public_url)   
        dct ={
            "file_url": public_url, 
            "is_error": False, 
            "error": None, 
            "df_sample": str(df.head(3)),
            "rfp_dct": rfp_dct
        }
        return json.dumps(dct)
    except Exception as e:
        dct ={
            "file_url": None, 
            "is_error": True, 
            "error": e, 
            "df_sample": None,
            "rfp_dct": rfp_dct
        }
        return dct
