"""
hypothesis.py

This file contains functions that you must implement.

IMPORTANT INSTRUCTIONS:
    - Do NOT modify the function signatures of the functions in this file.
    - Only make changes inside the specified locations for your implementation.
    - You may add additional helper functions if you wish.
    - Do NOT import anything other than what is already imported below.
"""

import pandas as pd
from typing import Tuple, List
from scipy.stats import ttest_ind


def multi_ttest(
    filtered_features: pd.DataFrame,
    label_df: pd.DataFrame,
    column_substring: str,
    alpha: float = 0.05,
) -> Tuple[pd.DataFrame, List[str]]:
    """
    Performs a t-test on each column in the filtered_features dataframe
    whose name contains the column_substring to test it's association with
    the death_in_stay outcome. Returns a dataframe containing three columns:
    column_name, p_value, and a boolean column indicating whether the null
    hypothesis was rejected for that column when compared to a bonferroni
    corrected significance level, and returns a list containing the string
    column names of the features that were found to have a significant
    association with the death_in_stay outcome.

    IMPLEMENTATION INSTRUCTIONS:
        - Implement the function below where specified.
        - Perform a t-test on each column in the filtered_features dataframe
            whose name contains the column_substring.
        - Store the column name, p-value, and a boolean indicating whether the
            null hypothesis was rejected for that column in a dataframe.
        - The returned dataframe should have three columns:
            - column_name: The name of the column
            - p_value: The p-value of the t-test
            - reject_null: A boolean indicating whether the null hypothesis was
                rejected for that column when compared to a bonferroni corrected
                significance level.
        - Use the ttest_ind function from scipy.stats to perform the t-tests.
            (already imported for you)
        - Use a bonferroni corrected significance level of alpha / num_columns
            when determining whether to reject the null hypothesis for a column.
        - Do NOT modify the input dataframes.

    Parameters:
        filtered_features (pd.DataFrame): A dataframe containing the filtered
            features
        label_df (pd.DataFrame): A dataframe containing the labels
        column_substring (str): A substring that will be used to filter the
            columns to perform t-tests on
        alpha (float): The (uncorrected) significance level to use when determining
            whether to reject the null hypothesis for a column.

    Returns:
        ttest_results (pd.DataFrame): A dataframe containing the results of the
            t-tests
        sig_columns (List[str]): A list containing the string column names of the

    """

    # Overwrite these variables with your implementation
    ttest_results = None

    sig_columns = []


    # ==================== YOUR CODE HERE ====================
    
    # TODO: Implement
    # Make copies to avoid modifying original dataframes
    features_copy = filtered_features.copy().reset_index()
    labels_copy = label_df.copy().reset_index()

    # Merge features with labels
    merged_df = pd.merge(
        features_copy,
        labels_copy,
        on='subject_id',
        how='inner'
    )

    # Get columns that contain the substring
    feature_columns = [col for col in filtered_features.columns
                       if column_substring in col]

    # Calculate Bonferroni corrected alpha
    num_columns = len(feature_columns)
    bonferroni_alpha = calc_bonferroni(alpha, num_columns)

    # Initialize lists to store results
    results = []

    # Perform t-test for each column
    for column in feature_columns:
        # Split data into groups
        survived_values = merged_df[merged_df['death_in_stay'] == 0][column]
        deceased_values = merged_df[merged_df['death_in_stay'] == 1][column]

        # Perform t-test
        _, p_value = ttest_ind(survived_values, deceased_values)

        # Check if null hypothesis should be rejected
        reject_null = p_value < bonferroni_alpha

        # Store results
        results.append({
            'column_name': column,
            'p_value': p_value,
            'reject_null': reject_null
        })

        # If significant, add to significant columns list
        if reject_null:
            sig_columns.append(column)

    # Create results DataFrame
    ttest_results = pd.DataFrame(results)

    # Sort results by p-value
    ttest_results = ttest_results.sort_values('p_value')
    
    # ==================== YOUR CODE HERE ====================
    

    return ttest_results, sig_columns


def calc_bonferroni(original_alpha: float = 0.05, number_of_test: int = 1) -> float:
    """
    Calculates the bonferroni corrected significance level for a given original
    significance level and number of tests.

    IMPLEMENTATION INSTRUCTIONS:
        - Implement the function below where specified.
        - Calculate the bonferroni corrected significance level for a given
            original significance level and number of tests.
        - Return the bonferroni corrected significance level.

    Parameters:
        original_alpha (float): The original significance level
        number_of_test (int): The number of tests

    Returns:
        bonferroni_alpha (float): The bonferroni corrected significance level
    """

    # Overwrite this variable with your implementation
    bonferroni_alpha = None


    # ==================== YOUR CODE HERE ====================
    
    # TODO: Implement
    bonferroni_alpha = original_alpha / number_of_test
    
    # ==================== YOUR CODE HERE ====================
    

    return bonferroni_alpha
