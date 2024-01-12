from promptflow import tool


# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def extract_rfp(chat_hist) -> str:
    rfp = chat_hist[0].get('outputs').get('answer').split('\n### 要件定義 ###\n')[-1]
    return rfp
