from promptflow import tool
import json


@tool
def generate_response(input1=None, input2=None, input3=None) -> str:

    if input1 is not None:
        return input1
    elif input2 is not None and not input2.get('hasConfirm'):
        comment = "以下の要件を確認してください。問題がなければOK、修正が必要な場合は修正内容を記述してください。\n### 要件定義 ###\n"
        return comment + input2.get('rfp')
    elif input3 is not None:
        dct = json.loads(input3)
        if not dct.get('is_error', True):
            comment = "以下のURLにデータを出力しました。"
            file_url = dct['file_url']
            sample = dct['df_sample']
            rfp_str = "\n".join(f"[{key}]\n{value}\n" for key, value in dct['rfp_dct'].items())
            response = comment + "\n" + file_url + "\nサンプルデータ\n" + sample + "\n仕様\n" + rfp_str 
        else:
            comment = "SQLエラー"
            query = dct['rfp_dct']['クエリ']
            error = dct['err']
            response = comment + "\nerror\n" + error + "\nクエリ\n" + query
        return response
    else:
        return 'no data'