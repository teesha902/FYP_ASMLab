# Functions necessary to create master dataframe
# Use the calls below to see how to use this functions

import pandas as pd
import numpy as np


def find_consecutive_subsets(lst, n):
    """
    This function iterates through all possible subsets of length n in a list. (its inefficient but its fast and it works)
    If the subset is consecutive, it is added to a list of subsets.
    The check for consecutive is done by checking if the difference between the last and first element is n-1.
    The function returns the list of subsets.
    """
    subsets = []
    start = 0
    while start <= len(lst) - n:
        # print(start)
        subset = lst[start:start+n]
        if subset[-1] - subset[0] == n -1 : # check if the subset is (nearly) consecutive by checking if the difference between the last and first element is ___
            subsets.append([subset[0],subset[-1]])
        start += 1
    return subsets

def find_subset(df, start_frame, subset_length, debug = False):
    """
    Creates a list of valid frames before LED start frame. Invalid frames are frames where all likelihood < 0.25 or na, or jittery frames.
    Then, it finds the valid subsets of frames before LED start frame.
    Returns a random subset of length subset_length from the list of valid subsets.
    """
    # generate the valid subset of frames before LED start frame
    print("led start frame", start_frame) if debug else None
    # columns_to_check are likelihood col, jitter col. We do likelihood check first
    valid_cols = [col for col in df.columns if "likelihood" in col or "jittery" in col]
    likelihood_cols = [col for col in df.columns if "likelihood" in col]
    bef_led_df = df.loc[150:int(start_frame), valid_cols] #exclude first 5 seconds of video
    # print(bef_led_df.head(5))
    # an valid frame is any frame where all likelihood > 0.25 or not nan
    valid_frames = bef_led_df[likelihood_cols] > 0.25 
    # find rows where <=2 false values (i.e. 2 bodyparts or less likelihood < 0.25 or nan), aka 3 reliable body parts
    valid_frames = valid_frames.sum(axis=1) >= 3 # we sum true values and check whether number of true values >= 2
    valid_frames = valid_frames[valid_frames == True].index.tolist()    
    print("valid frames len", len(valid_frames)) if debug else None
    jitter_df = bef_led_df["jittery"]
    print("jittery frames", len(jitter_df[jitter_df == 1])) if debug else None
    jitter_df = jitter_df[jitter_df == 0]
    no_jitter_frames = jitter_df.index.tolist()
    valid_frames.extend(no_jitter_frames)
    valid_frames = list(sorted(set(valid_frames)))
    valid_subsets = find_consecutive_subsets(valid_frames, int(subset_length))
    return valid_subsets



def create_master_dataframe(columns, csv_files, led_csv, random_pre_led = False, debug = False):
    # create a dict with the columns as keys
    data = {f"{col}": [] for col in columns}
    for csv in csv_files:
        print(csv.name)
        led_row = led_csv[led_csv["name"].str.contains(csv.stem)]

        if led_row.empty:
            print(f"LED file not found for {csv.name}")
            continue

        df = pd.read_csv(csv)
        led_start_frame, led_end_frame = led_row["start frame"].values[0] - 1, led_row["end frame"].values[0] - 1 # -1 because of 0 indexing
        # led_x, led_y = led_row["x"].values[0], led_row["y"].values[0]


        if random_pre_led:
            subset_length = led_end_frame - led_start_frame
            print("subset length:", subset_length) if debug else None
            # find the subset of same length as led data before led data
            subsets = find_subset(df, led_start_frame, subset_length)
            print("subsets len", len(subsets)) if debug else None
            if len(subsets) == 0:
                print("no valid subset found for ", csv.name)
                continue
            print(subsets) if debug else None
            subset = random.choice(subsets)
            # print(start_frame, end_frame)
            start_frame, end_frame = subset[0], subset[-1]
        else:
            start_frame, end_frame = led_start_frame, led_end_frame   
    # print(start_frame, end_frame)
        name = csv.stem.split("_")[1]
        data["name"].append(name) if "name" in columns else None
        control_uro = 1 if "uro" in str(csv) else 0
        data["uroa_control"].append(control_uro) if "uroa_control" in columns else None
        day = csv.parent.name
        data["day"].append(int(day)) if "day" in columns else None
        dist = df.loc[start_frame:end_frame, "avg_dist_vel"].sum()
        data["dist"].append(dist) if "dist" in columns else None
        avg_vel = df.loc[start_frame:end_frame, "avg_dist_vel"].mean()
        data["vel"].append(avg_vel) if "vel" in columns else None
        avg_acc = df.loc[start_frame:end_frame, "avg_acc"].mean()
        data["acc"].append(avg_acc) if "acc" in columns else None
        avg_angle = df.loc[start_frame:end_frame, "angle"].mean()
        data["head_angle"].append(avg_angle) if "head_angle" in columns else None
        max_dist_surface = df.loc[start_frame:end_frame, "distance_surface"].max()
        data["dist_surface"].append(max_dist_surface) if "dist_surface" in columns else None

        frames_y = df.loc[start_frame:end_frame, [col for col in df.columns if "_y" in col]].mean(axis=1)
        frames_x = df.loc[start_frame:end_frame, [col for col in df.columns if "_x" in col]].mean(axis=1)
        
        y_initial, x_initial = frames_y.iloc[0], frames_x.iloc[0]
    
        count_above_y_initial = frames_y[frames_y > y_initial].count().sum()
        percent_above_y_initial = count_above_y_initial *100 / len(frames_y)
        data["y_up"].append(percent_above_y_initial) if "y_up" in columns else None
    
        # find frame where y is highest
        y_max_frame = frames_y.idxmax()
        # print(y_max_frame)
        y_mag = frames_y.loc[y_max_frame] - y_initial
        # x_mag = frames_x.loc[y_max_frame] - x_initial
        data["y_mag"].append(y_mag) if "y_mag" in columns else None
    
        # trajectory_angle is the angle between the initial and highest point of the trajectory using the x and the y axis
        y_max = frames_y.loc[y_max_frame]
        x_max = frames_x.loc[y_max_frame]
        # print( y_max, x_max, y_initial, x_initial)
        trajectory_angle = np.arctan2([y_max - y_initial], [x_max - x_initial])[0] * 180 / np.pi
        trajectory_angle = trajectory_angle if trajectory_angle > 0 else trajectory_angle + 360
        data["trajectory_angle"].append(trajectory_angle) if "trajectory_angle" in columns else None

        data["start_y_from_led"].append(df.loc[start_frame, "distance_surface"]) if "start_y_from_led" in columns else None

        # trajectory angle till end of led using frames_y and frames_x
        end_trajectory_angle = np.arctan2([frames_y.iloc[-1] - y_initial], [frames_x.iloc[-1] - x_initial])[0] * 180 / np.pi        
        end_trajectory_angle = end_trajectory_angle if end_trajectory_angle > 0 else end_trajectory_angle + 360
        data["end_trajectory_angle"].append(end_trajectory_angle) if "end_trajectory_angle" in columns else None

    
    
    
    for key, value in data.items():
        print(key, len(value))
    data_df = pd.DataFrame(data)
    print(data_df.head(5))
    return data_df


# function to generate n number of before led dfs and combine to return the one avg df

def create_averaged_before_led_df(n, columns, csv_files, led_csv, random_pre_led, debug):
    # create n number of before led dfs
    before_led_dfs = []
    for i in range(n):
        i_before_led_df = create_master_dataframe(columns, csv_files, led_csv, random_pre_led = random_pre_led, debug = debug)
        before_led_dfs.append(i_before_led_df)
    # combine the before led dfs into one df
    before_led_df = pd.concat(before_led_dfs)
    # get the average of the before led dfs
    before_led_df = before_led_df.groupby(["name", "uroa_control", "day"]).mean().reset_index()
    return before_led_df
