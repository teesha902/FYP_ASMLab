import pandas as pd 
import numpy as np
from scipy.spatial.distance import pdist


def distance_vel(df, debug):
    """ calculate the distance travelled between frames for each body part"""
    print("Calculating distance (same as vel)") if debug else None

    # define X and Y columns to apply the different conversion
    x_columns = [col for col in df.columns if "_x" in col]
    y_columns = [col for col in df.columns if "_y" in col]
    likelihood_columns = [col for col in df.columns if "likelihood" in col]

    for (x,y) in zip(x_columns, y_columns): #iterate over body part
        # caluclate the distance between last frame and current frame for bodypart
        # column name is {bodypart}_dist
        df[f'{x.split("_")[0]}_dist'] = np.sqrt((df[x].diff())**2 + (df[y].diff())**2)
    weights = df[likelihood_columns] #.astype(float)
    #using masked average to avoid null values
    df["avg_dist_vel"] = np.average( df[[col for col in df.columns if "dist" in col]], axis=1, weights = weights)          
    
    print(df.head(5)) if debug else None
    return df

def acc(df, fps, debug):
    """the velocity and acceleration are calculated using the distance columns"""
    # fps 
    print("Calculating acceleration") if debug else None
    time_per_frame = 1/fps

    df["avg_acc"] = df["avg_dist_vel"] / time_per_frame

    print(df.head(5)) if debug else None
    return df