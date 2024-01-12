rm -rf .venv
poetry cache clear --all pypi
/Volumes/EXTERNAL_SSD/hirayamayuuzou/Documents/chatGPT/query_chat_pf/chat-flow/.venv/bin/python -m pip install --upgrade pip

poetry install



/Volumes/EXTERNAL_SSD/hirayamayuuzou/.pyenv/versions/3.10.9/bin/python -m promptflow._cli._pf.entry run create --flow /Volumes/EXTERNAL_SSD/hirayamayuuzou/Documents/chatGPT/chat-flow/chat-flow --data /Volumes/EXTERNAL_SSD/hirayamayuuzou/Documents/chatGPT/chat-flow/chat-flow/.promptflow/data.jsonl --stream
