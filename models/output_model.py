from pydantic import BaseModel, Field
from typing import List
import json

# class Task(BaseModel):
#     tasks: List[str] = Field(description="Hypothesis to achieve the goal")
# class SQLResponse(BaseModel):
#     SQLQuery: str = Field(description="SQL Query to run")


class TextParser:
    def __init__(self, text):
        self.text = text
        self.extracted_data = self._extract_data()

    def _extract_data(self):
        extracted_data = {}
        lines = self.text.split("\n")
        current_key = None
        current_value = []

        for line in lines:
            if ':' in line and (not current_key or current_key and current_value):
                if current_key:
                    extracted_data[current_key] = "\n".join(current_value).strip()
                current_key = line.split(':', 1)[0].strip()
                current_value = [line.split(':', 1)[1].strip()] if len(line.split(':', 1)) > 1 else []
            elif current_key is not None:
                current_value.append(line)

        if current_key:
            extracted_data[current_key] = "\n".join(current_value).strip()

        return extracted_data


    def get_value(self, key):
        return self.extracted_data.get(key)