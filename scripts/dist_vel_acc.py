import pandas as pd 
import numpy as np


def distance(df, x_columns, y_columns, debug):
    """ calculate the distance travelled between frames for each body part"""
    for (x,y) in zip(x_columns, y_columns): #iterate over body part
        # caluclate the distance between last frame and current frame for bodypart
        # column name is dist_{bodypart}
        diff_x = df[x].diff()
        diff_y = df[y].diff()
        df[f'dist_{x.split("_")[0]}'] = np.sqrt((diff_x)**2 + (diff_y)**2)
        # df[f'dist_{x.split("_")[0]}'] = np.sqrt((df[x].diff)**2 + (df[y].diff())**2)          
    print(df.head(5)) if debug else None
    return df

def dist_vel_acc(df, fps, debug):
    """ calculate the distance, velocity and acceleration of the data.
    distance() is called first to calculate the distance between frames
    then the velocity and acceleration are calculated using the distance columns"""

    # define X and Y columns to apply the different conversion
    x_columns = ["Tail_x", "Body1_x", "Body2_x", "Body3_x", "Head_x"]
    y_columns = ["Tail_y", "Body1_y", "Body2_y", "Body3_y", "Head_y"]
    
    print("Calculating distance, velocity and acceleration")
    print(df.head(5)) if debug else None

    # fps 
    time_per_frame = 1/fps
    # calculate the distance
    df = distance(df, x_columns, y_columns, debug)
    # calculate the velocity using distance columns
    for column in df.columns:
        if column.startswith('dist_'):
            # calculate the velocity using distance columns
            # split column name to get the body part name
            df[f'vel_{column.split("_")[-1]}'] = df[column].diff() / time_per_frame
            # calculate the acceleration using velocity columns
            df[f'acc_{column.split("_")[-1]}'] = df[f'vel_{column.split("_")[-1]}'].diff() / time_per_frame

    print(df.head(5)) if debug else None
    return df