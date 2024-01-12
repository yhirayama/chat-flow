from typing import List, Dict

class DataModel:
    def __init__(self, data: Dict):
        self.data = data

    def get_columns(self) -> List[str]:
        """
        Get the columns of the data.

        Returns:
        - List[str]: List of columns.
        """
        return list(self.data.keys())

    def get_summary(self) -> Dict:
        """
        Get a summary of the data.

        Returns:
        - Dict: Summary statistics of the data.
        """
        # This is a placeholder. In a real-world scenario, you might compute summary statistics.
        return self.data
