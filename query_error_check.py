from promptflow import tool
import json

@tool
def my_python_tool(input1: dict) -> bool:
    dct = json.loads(input1)
    return dct.get('is_error')
