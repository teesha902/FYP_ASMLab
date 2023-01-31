import pandas as pd 
import numpy as np
from scipy.spatial.distance import pdist


def distance(df, debug):
    """ calculate the distance travelled between frames for each body part"""
    # define X and Y columns to apply the different conversion
    x_columns = ["Tail_x", "Body1_x", "Body2_x", "Body3_x", "Head_x"]
    y_columns = ["Tail_y", "Body1_y", "Body2_y", "Body3_y", "Head_y"]
    for (x,y) in zip(x_columns, y_columns): #iterate over body part
        # caluclate the distance between last frame and current frame for bodypart
        # column name is {bodypart}_dist
        df[f'{x.split("_")[0]}_dist'] = np.sqrt((df[x].diff())**2 + (df[y].diff())**2)          
    print(df.head(5)) if debug else None
    return df

def vel_acc(df, fps, debug):
    """the velocity and acceleration are calculated using the distance columns"""

    print("Calculating velocity and acceleration") if debug else None
    
    # fps 
    time_per_frame = 1/fps
    # calculate the velocity using distance columns
    for column in df.columns:
        if "dist" in column:
            # calculate the velocity using distance columns
            # split column name to get the body part name
            df[f'{column.split("_")[0]}_vel'] = df[column] / time_per_frame
            # calculate the acceleration using velocity columns
            df[f'{column.split("_")[0]}_acc'] = df[f'{column.split("_")[0]}_vel'] / time_per_frame

    print(df.head(5)) if debug else None
    return df