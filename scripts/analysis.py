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

    # weights df using likelihood
    weights = df[likelihood_columns]
    weights = weights.fillna(0)
    # normalise the weights to sum to 1
    weights_norm = weights.div(weights.sum(axis=1), axis=0) 
    # distance df
    dist_columns = [col for col in df.columns if "_dist" in col]
    dist_df = df[dist_columns]
    # remove rows where all values are nan. The mask is created now, but the step is done at the end
    row_mask = dist_df.isnull().all(axis=1)
    dist_df = dist_df.fillna(0)

    # calculate the weighted average of the distance columns
    df["avg_dist_vel"] = np.average(dist_df, axis=1, weights = weights_norm)
    # find rows in row mask and set those rows to na
    df.loc[row_mask, "avg_dist_vel"] = np.nan
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

def tail_head_angle(df, debug):
    ''' 
    Calculate the angle between the tail and the head
    '''
    print("Calculating angle") if debug else None
    # define X and Y columns to apply the different conversion
    x_columns = ["Head_x", "Tail_x"]
    y_columns = ["Head_y", "Tail_y"]
    df["angle"] = np.arctan2(df[y_columns[0]] - df[y_columns[1]], df[x_columns[0]] - df[x_columns[1]]) * 180 / np.pi
    # convert the negative angles to positive
    df["angle"] = df["angle"].apply(lambda x: x if x >= 0 else 360 + x) # its positive because the angle itself is negative
    print(df.head(5)) if debug else None
    return df

def distance_led(df, led_y, debug):
    """ calculate the distance between the led and the fish
    this outputs a column with averaged y distance of body parts from led-y
    for values below 0 (implying fish is above LED), set to nan and mark as jittery
    """

    print ("Calculating distance from surface") if debug else None

    y_columns = [col for col in df.columns if "_y" in col]
    # surface = df[y_columns].max(axis=0).mean()
    # df["distance_surface"] = surface - df[y_columns].average(axis=0)
    df["distance_surface"] = (df[y_columns].mean(axis=1) - led_y)

    # set negative values to nan and mark as jitter in the jitter column
    df.loc[df["distance_surface"] > 0, ["distance_surface", "jittery"]] = [None, 1]
    print(df.head(5)) if debug else None
    return df