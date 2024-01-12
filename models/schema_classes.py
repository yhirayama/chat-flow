class Field:
    """BigQueryのフィールドを表すクラス"""
    def __init__(self, name, field_type, description):
        self.name = name
        self.field_type = field_type
        self.description = description

    def __str__(self):
        return f"    {self.name}: {self.description}"

class Table:
    """BigQueryのテーブルを表すクラス"""
    def __init__(self, table_id, description, schema, dataset):
        self.table_id = table_id
        self.description = description
        self.schema = [Field(field.name, field.field_type, field.description) for field in schema]
        self.dataset = dataset
    
    def __str__(self):
        # table_id を {dataset_id}.{table_id} の形式に整形
        formatted_table_id = f"{self.dataset.dataset_id}.{self.table_id}"
        fields_str = "\n".join(str(field) for field in self.schema)
        return f"table_id: {formatted_table_id}\nfields:\n{fields_str}"

class Dataset:
    """BigQueryのデータセットを表すクラス"""
    def __init__(self, dataset_id, description, tables):
        self.dataset_id = dataset_id
        self.description = description
        self.tables = tables

    def __str__(self):
        tables_str = "\n\n".join(str(table) for table in self.tables)
        return tables_str
    
    def get_table_by_id(self, table_id):
        """指定した table_id に一致するテーブルを取得するメソッド。

        Args:
            table_id (str): 取得したいテーブルの ID

        Returns:
            Table or None: テーブルが見つかった場合は Table クラスのインスタンスを返し、見つからない場合は None を返す
        """
        for table in self.tables:
            if table.table_id == table_id:
                return table
        return None