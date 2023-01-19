"""
Defines data check functions which will be used by the main integrity_inter_mm_analysis.py script

Sample dataframe for dlc csv files (the df should be passed in this format to the functions):

bodyparts Tail  Tail Tail       Body1 Body1 Body1 ...
coords    x     y    likelihood x     y     likelihood ...
0         187.0 10.0 0.681      228.0 99.6  0.2879999 ...


Functions:
check_blanks checks for an overall percentage of missing data and low likelihood data in the dataframe
long_blanks checks for a long period of missing data or low likelihood in the dataframe
jittery_moves checks for jittery moves in the dataframe by comparing distance travelled between frames to threshold

Created by: Aritejh
"""

import pandas as pd
import numpy as np
import glob
import os

def check_overall(df, threshold, debug = False):
    """
    Checks for an overall percentage of missing data and low likelihood data in the dataframe
    uses threshold for likelihood
    """
    # Get the number of missing values in each column
    missing_values_count = sum(df.isnull().sum()) 
    print(missing_values_count, "missing values") if debug else None
    # Total number of cells in the dataframe
    total_cells = np.product(df.iloc[2:, 1:].shape) #exclude headers and frame column
    # low likelihood count
    low_likelihood_count_df = df.iloc[2:, 3::3].astype(float)
    low_likelihood_count = sum(low_likelihood_count_df[low_likelihood_count_df <= threshold].count())
    print(low_likelihood_count, "low likelihood values") if debug else None
    # Total number of missing values
    total_missing = missing_values_count + low_likelihood_count*3 #multiply by 3 because there are 3 columns per body part
    # Percentage of missing values
    percent_missing = (total_missing/total_cells) * 100
    return percent_missing

def get_invalids(df, threshold, debug = False):
    """
    Checks for a missing data or low likelihood in the dataframe, uses threshold for likelihood.
    returns a list of the invalid frames for each body part
    """
    blanks = []
    no_cols = len(df.columns)
    #choose 3 columns to check for missing data 
    for i in range(1, no_cols, 3): 
        part_df = df.iloc[:, i:i+3]
        print(part_df.head(5)) if debug else None
        # Get the list of rows with missing values in any column
        missing_values = part_df[part_df.isnull().any(axis=1)].index.tolist()
        print(missing_values) if debug else None
        # Get the list of low likelihood values in each column
        part_likelihood = part_df.iloc[2:,-1].astype(float)
        low_likelihood = part_likelihood.index[part_likelihood <= threshold].tolist()
        print(low_likelihood) if debug else None
        # Combine the two lists
        part_missing = list(np.unique(np.sort(np.concatenate((missing_values, low_likelihood)))))
        blanks.append(part_missing) 
    return blanks

def jittery_moves(df, threshold):
    """
    Checks for jittery moves in the dataframe by comparing distance travelled between frames
    to threshold. Returns a list of jittery frames
    """
    # Get the distance travelled between frames
    distance = df.diff()
    # Get the frames where the distance travelled is greater than the threshold
    jittery_frames = distance[distance > threshold].index.tolist()
    return jittery_frames

# df = pd.read_csv("data/csv/test_csv.csv", header=None)
# print(df.head(5))
# print(long_blanks(df, 10))