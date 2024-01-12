from promptflow import tool
import json


# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(input1: dict, target_key: str, rfp="", rfp2="") -> dict:
    dct = json.loads(input1.get("function_call").get("arguments"))
    hasConfirm = dct.get(target_key)
    if rfp2 == "":
        rfp_out = rfp
    else:
        rfp_out = rfp2
    out = {
        "hasConfirm":hasConfirm, 
        "rfp":rfp_out
        }
    return out
