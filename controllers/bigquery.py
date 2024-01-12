import os
import csv
import json
import csv
from dotenv import load_dotenv
from google.cloud import bigquery, storage
from google.oauth2 import service_account
import pandas as pd

from models.schema_classes import Table, Dataset
import logging
import tempfile

logger = logging.getLogger(__name__)


# bigqueryの設定
# configから呼ぶようにする
load_dotenv()
service_account_path = os.getenv("GCP_SERVICE_ACCOUNT_PATH")
credentials = service_account.Credentials.from_service_account_file(service_account_path)
project_id = credentials.project_id
client = bigquery.Client(credentials=credentials, project=project_id)
gcs_client = storage.Client(credentials=credentials, project=project_id)


# sql実行
def exe_query(query:str) -> pd.DataFrame:
    client = bigquery.Client(credentials=credentials, project=project_id)
    query_job = client.query(query)  # Make an API request.
    return query_job.to_dataframe()


def get_schemas_in_datasets(datasets:list) -> str:
    """_summary_
    指定のdatasetsに含まれるテーブルのスキーマを取得する
    """
    datasets_list = []
    for dataset in client.list_datasets():
        if dataset.dataset_id in datasets:
            dataset_ref = client.dataset(dataset.dataset_id)
            dataset_obj = client.get_dataset(dataset_ref)
            dataset_instance = Dataset(dataset_obj.dataset_id, dataset_obj.description)
            
            for table in client.list_tables(dataset_ref):
                table_ref = dataset_ref.table(table.table_id)
                table_obj = client.get_table(table_ref)
                dataset_instance.tables.append(Table(table_obj.table_id, table_obj.description, table_obj.schema))

            datasets_list.append(dataset_instance)

    return datasets_list


def get_dataset_metadata(dataset_id):
    """BigQueryのメタデータを取得し、Dataset クラスのインスタンスを返す関数。

    Args:
        dataset_id (str): データセットの ID

    Returns:
        Dataset: Dataset クラスのインスタンス
    """
    try:
        # dataset のメタデータを取得
        dataset_metadata = client.get_dataset(dataset_id)

        # table のメタデータを取得
        tables_metadata = client.list_tables(dataset_id)

        # Table クラスのインスタンスを作成
        tables = []
        for table_metadata in tables_metadata:
            table = client.get_table(table_metadata.reference)
            tables.append(Table(table.table_id, table.description, table.schema, dataset_metadata))

        # Dataset クラスのインスタンスを作成
        dataset = Dataset(dataset_metadata.dataset_id, dataset_metadata.description, tables)

        return dataset
    except Exception as e:
        print("An error occurred:", str(e))


def upload_dataframe_to_gcs(df, bucket_name, destination_blob_name):
    """
    DataFrameをGoogle Cloud Storageにアップロードし、公開URLを取得する関数。

    Args:
    df (pandas.DataFrame): アップロードするDataFrame。
    bucket_name (str): アップロード先のGCSバケット名。
    destination_blob_name (str): GCS内のファイル名。

    Returns:
    str: アップロードされたファイルの公開URL。
    """

    # 一時ファイルにDataFrameをCSVとして保存
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.csv', delete=True) as temp_file:
        df.to_csv(temp_file.name, index=False)

        # GCSにアップロードするためのクライアントを初期化
        client = gcs_client
        bucket = client.get_bucket(bucket_name)

        # CSVをバケットにアップロード
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(temp_file.name)

        # ファイルを公開状態に設定
        # blob.make_public() # パブリックにするには公開可能に設定する必要あり

        # 公開URLの取得
        return blob.public_url



if __name__ == '__main__':
    # datasets = get_datasets_and_schemas()
    # 結果を出力して確認
    
    df = pd.DataFrame({'data': [1, 2, 3]})
    bucket_name = 'your-bucket-name'
    destination_blob_name = 'my_data.csv'

    public_url = upload_dataframe_to_gcs(df, bucket_name, destination_blob_name)
    print(public_url)    
    # dataset = get_bigquery_metadata(dataset_id)
    # table = dataset.get_table_by_id(table_id)
    # print(table)