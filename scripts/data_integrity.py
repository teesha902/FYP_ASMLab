"""
Defines data check functions which will be used by the main integrity_inter_mm_analysis.py script

Sample dataframe for dlc csv files (the df should be passed in this format to the functions):

bodyparts_coords Tail_x  Tail_y Tail_likelihood ...
0                187.0   10.0   0.681      ...


Functions:
check_overall checks for an overall percentage of missing data and low likelihood data in the dataframe.
get_invalids returns list of invalid frames for a missing data or low likelihood in the dataframe, uses threshold for likelihood. Replaced with direct replacement in data_mm_analyse.py.
jittery_moves checks for jittery moves in the dataframe by comparing distance travelled between frames to threshold

Created by: Aritejh
"""

import pandas as pd
import numpy as np
import glob
import os
from math import sqrt
from scipy.spatial.distance import pdist

def check_overall(df, threshold, debug = False):
    """
    Checks for an overall percentage of missing data and low likelihood data in the dataframe
    uses threshold for likelihood
    """
    # Get the number of missing values in each column
    missing_values_count = sum(df.isnull().sum()) 
    print(missing_values_count, "missing values") if debug else None
    # Total number of cells in the dataframe
    total_cells = np.product(df.iloc[:, 1:].shape) #exclude headers and frame column
    # low likelihood count
    low_likelihood_count_df = df.iloc[:, 3::3].astype(float)
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
    returns a list of the invalid frames for each body part. [[...],[...],[...],[...],[...]]
    NOT USED ANYMORE BUT KEPT FOR FUTURE USE
    """
    blanks = []
    no_cols = len(df.columns)
    #choose 3 columns to check for missing data 
    for i in range(1, no_cols, 3): # remove the frame column
        part_df = df.iloc[:, i:i+3] # get the 3 columns for each body part
        print(part_df.head(5)) if debug else None 
        # Get the list of rows with missing values in any column
        missing_values = part_df[part_df.isnull().any(axis=1)].index.tolist()
        print(missing_values) if debug else None
        # Get the list of low likelihood values in each column
        part_likelihood = part_df.iloc[:, -1].astype(float)
        low_likelihood = part_likelihood.index[part_likelihood <= threshold].tolist()
        print(low_likelihood) if debug else None
        # Combine the two lists
        part_missing = list(np.unique(np.sort(np.concatenate((missing_values, low_likelihood)))))
        blanks.append(part_missing)
    # print the percentage of invalid frames on average
    return blanks

def jittery_frames(df, debug):
    """
    Checks for jittery moves in the dataframe by checking fish length .
    Fish length is calculated using avg distance between points. 
    Returns a list of jittery frames
    """
    # drop frame and likelihood columns
    coords_df = df.drop(df.columns[[0,3,6,9,12,15]], axis=1)
    print(coords_df.head(5)) if debug else None

    # convert the dataframe to float values
    coords_df = coords_df.astype(float)
    # initialize problem frames and fish length list
    problem_frames = []
    fish_length = []
    # iterate through rows to extract info
    for row in coords_df.itertuples():
        x = [row[i] for i in range(1,10,2)]
        y = [row[i] for i in range(2,11,2)]
        points = np.array([[x[i], y[i]] for i in range(0, len(x))])
        distances = np.round(pdist(points, metric='euclidean'),2)
        if sum(distances)/len(distances):
            fish_length.append(sum(distances)/len(distances)) # this metric may be inaccurate, as high distance can also be points missing in the middle
    
    # check if fish length list is not empty
    if len(fish_length) > 0:
        # remove nan values from fish length list
        fish_length = [x for x in fish_length if str(x) != 'nan']
        # calculate the histogram of fish length
        hist, bin_edges = np.histogram(fish_length, range = (0, max(fish_length)), bins = 100)
        # find the first bin that has zero values
        for i, prob in enumerate(hist):
            if prob == 0 and i >10:
                break
        print(bin_edges[i]) if debug else None
        threshold = bin_edges[i]
        # add frames with fish length greater than threshold to problem frames list
        [problem_frames.append(i) for frame, fish_length in enumerate(fish_length) if fish_length > threshold]
    print(f"{len(problem_frames)*100/len(fish_length):.2f}% of frames are jittery")
    return problem_frames
