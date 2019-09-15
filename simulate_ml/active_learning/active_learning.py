import pandas as pd
import numpy as np

class ActiveLearner:
    def __init__(self):
        pass

    def get_label_datatype(self, label_column: str) -> str:
        """
        Get the data type for the label column.
        """
        label_type = input(f"""
        What type of data should the label column be?
        Here's the label column's name for reference: {label_column}
        You have the following options:
        * string
        * integer 
        * float
        """)
        supported_types = [
            "string",
            "integer",
            "float",
        ]
        if label_type not in supported_types:
            raise Exception(f"""
            {label_type} not in {supported_types}
            Please provide one of these: {supported_types}
            """)
        return label_type

    def ask_user_for_labels(self, null_data, columns_to_use, label_type):
        """
        Explicitly ask the user for the labels.
        """
        labels = []
        for _, null_datum in null_data.iterrows():
            for col in columns_to_use:
                print(col,":", null_datum[col])
            label = input("What label should the above data have?")
            if label_type != "string":
                label = float(label)
            labels.append(label)
        return labels

    def process_columns_to_use(self, columns_to_use):
        """
        Decide which columns to use for labeling.
        """
        if columns_to_use == []:
            columns_to_use = null_data.columns.tolist()
            columns_to_use.remove(label_column)
        return columns_to_use
    
    def hand_label(self, data: pd.DataFrame,
                   label_column: str,
                   columns_to_use: list = []) -> pd.DataFrame:
        """
        Hand label data.
        
        Returns
        -------
        * The data with labels from the hand labeling
        * the indexes in the original dataframe that were
        hand labeled
        """
        null_data = data[pd.isnull(data[label_column])]
        label_type = self.get_label_datatype(label_column)
        columns_to_use = self.process_columns_to_use(
            columns_to_use
        )
        labels = self.ask_user_for_labels(
            null_data, columns_to_use, label_type
        )
        data[label_column].iloc[null_data.index] = np.array(labels)
        return data, null_data.index

    def hand_label_n_times(self, data: pd.DataFrame,
                           label_column: str,
                           min_times_to_check: int = 5,
                           columns_to_use: list = [],
                           percent_to_check: float = 0.3) -> pd.DataFrame:
        """
        Hand label data, until the labels are consistent.
        
        Returns
        -------
        * The data with labels from the hand labeling
        * the indexes in the original dataframe that were
        hand labeled
        """
        percent_the_same = 0.0
        counter = 0
        while percent_the_same != 1.0:
            hand_labeled = self.hand_label(
                data, label_column, columns_to_use
            )
            results = self.check_hand_labeling(
                hand_labeled,
                label_column,
                columns_to_use,
                percent_to_check=percent_to_check
            )
            percent_the_same = results["percent_the_same"]
        # fix this more later - I should allow for
        # difference in labelling to change underlying label.

    def check_hand_labeling(self, data: pd.DataFrame,
                            hand_labeled_indices,
                            label_column,
                            columns_to_use,
                            percent_to_check=0.3):
        """
        Double check a percentage of hand labeled data.
        If the label the first time doesn't match the label
        the second time, then consider the data in question.
        If the label is the same both times, label has higher 
        confidence.
        """
        labeled_data = data.iloc[hand_labeled_indices]
        sample = labeled_data.sample(frac=percent_to_check)
        labels = sample[label_column]
        delabeled_sample = sample.copy()
        delabeled_sample[label_column] = np.nan
        labeled_sample, labeled_index = self.hand_label(
            delabeled_sample, label_column,
            columns_to_use
        )
        original_labels = labeled_data[label_column].iloc[labeled_index]
        new_labels = labeled_sample[label_column]
        num_equal = np.count_nonzero(orignal_labels == new_labels)
        return {
            "percentage_the_same": num_equal / len(sample)
            "count_the_same": num_equal
            "sample_size": len(sample)
        }
