"""
DOCUMENTATION
This script is used to convert the data from pixels to mm and perform data integrity checks.
It also performs the analysis of the data and saves the results in a csv file.
problematic csv files are saved in a problems_csv.txt file.

main() function: 
1. takes in the path to the csv files and the path to the LED csv file. 
2. for each csv file, it checks for LED data. This is needed for integrity checks specifically during LED duration.
3. The dataframe of the csv is reconstructed to have proper column names and numeric data type.
4. The dataframe is converted to mm.
5. The integrity checks such as missing data, low likelihood are performed. 
6 The analysis such as distance travelled, velocity. These are done first to enable 7.
7. The jittery moves are performed. This checks using sd of fish length and avg distance between keypoints.
8. LED time integrity checks take place.
9. acc, angle, distance_surface are calculated.
10. The results are saved in a csv file.

TODO:
- get fps from csv file
- improve jitter detection

Created by: Aritejh
"""

import numpy as np
import pandas as pd
import glob
import os
import argparse
from pathlib import Path
from scripts.analysis import distance_vel, acc, tail_head_angle, distance_led

from scripts.data_integrity import check_overall, jittery_frames

def convert_mm(name, df, debug):
    print(f"Converting: {name} to mm") if debug else None

    # define X and Y columns to apply the different conversion
    x_columns = [col for col in df.columns if "_x" in col]
    y_columns = [col for col in df.columns if "_y" in col]

    # Convert to mm
    df[x_columns] = df[x_columns] * 0.28
    df[y_columns] = df[y_columns] * -0.304

    print(df.head(5)) if debug else None
    return df


def main(csv_path, LED_csv, percent_missing_thresh, percent_low_likelihood_thresh, invalid_thresh, sd_threshold, output_path, debug):
    csv_files = list(csv_path.glob("**/*.csv"))

    problems_csv = []

    # print csv files
    print(len(csv_files), "csv files found")
    print(csv_files) if debug else None

    fps = 30 # TODO: get fps from csv file

    # Iterate through all csv files
    for csv_file in csv_files:
        # Read csv and create proper columns
        df = pd.read_csv(csv_file, header = None)
        print(csv_file.name)
        
        # get led time of the csv file
        led_row = LED_csv[LED_csv["name"].str.contains(csv_file.stem)]
        print(led_row) if debug else None
        led_absent = False # reset led_absent flag
        if led_row.empty:
            print(f"LED file not found for {csv_file.name}")
            problems_csv.append([csv_file.name, "LED file not found"])
            led_absent = True
        if not led_absent:
            start_frame, end_frame = led_row["start frame"].values[0] - 1, led_row["end frame"].values[0] - 1 # -1 because of 0 indexing
            led_x = led_row["x"].values[0] * 0.28 # convert to mm
            led_y = led_row["y"].values[0] * -0.304 # convert to mm
        df.columns = df.iloc[2] + "_" + df.iloc[3] # naming the columns as Tail_x, Tail_y, Tail_likelihood, etc.
        df.drop([0,1,2,3], inplace=True) # remove the first 4 rows. Contains model name, individual name, body part and x/y/likelihood
        df.reset_index(drop=True, inplace=True) # resets the row index
        print(df.head(5)) if debug else None
        
        # convert to numeric data type from str
        df = df.apply(pd.to_numeric, downcast = 'float' ,errors='coerce')

        # Convert to mm
        df = convert_mm(csv_file.name, df, debug)
        print(df.head(5)) if debug else None

        #check overall data integrity
        percent_missing, percent_low_likelihood = check_overall(df, invalid_thresh, debug)
        print(f"{percent_missing:.2f}% missing data, {percent_low_likelihood:.2f}% low likelihood data")
        
        if percent_missing > percent_missing_thresh:
            print(f"Too much missing data in {csv_file.name}")
            problems_csv.append([csv_file.name, percent_missing, "missing"])
        if percent_low_likelihood > percent_low_likelihood_thresh:
            print(f"Too much low likelihood data in {csv_file.name}")
            problems_csv.append([csv_file.name, percent_low_likelihood, "low_likelihood"])
        
        # replace <bodypart>_likelihood with 0 depending on if it is invalid or not. NOT NEEDED RN.
        # invalid frames are frames where the likelihood is less than the invalid_thresh or null
        likelihood_columns = [col for col in df.columns if "likelihood" in col]
        # df[likelihood_columns] = df[likelihood_columns].apply(lambda x: x.where(x.astype(float) >= invalid_thresh, 0).fillna(0))
        
        # need distance travelled to do jitter analysis
        df = distance_vel(df, debug)

        #check for jittery frames
        df = jittery_frames(df, sd_threshold, debug)

        # check for invalid/jittery frames in LED timing
        if not led_absent:
            print("checking for invalid frames in LED timing") if debug else None
            # check for invalid/jittery frames in LED timing
            mask_low_likelihood = df.loc[start_frame:end_frame, likelihood_columns] < invalid_thresh
            mask_absent = df.loc[start_frame:end_frame, likelihood_columns].isnull()
            combined = mask_low_likelihood | mask_absent
            print (combined.head(5)) if debug else None
            mask = combined.sum(axis=1) >= 4 # if more than 2 columns have low likelihood or absent
            print(mask.head(5)) if debug else None
            if len(combined.index[mask].tolist())/(end_frame-start_frame) > led_absent_thresh:
                print(f"{csv_file.name} contains > {led_absent_thresh * 100}% invalid frames in LED timing")
                problems_csv.append([csv_file.name, "invalid frames during LED", combined.index[mask].tolist()])

            mask_jitter = df.loc[start_frame:end_frame, "jittery"] == 1
            if len(mask_jitter.index[mask_jitter].tolist())/(end_frame - start_frame) > led_jitter_thresh:
                print(f" >10% Jittery frames in {csv_file.name} during LED timing")
                problems_csv.append([csv_file.name, "jittery frames during LED", mask_jitter.index[mask_jitter].tolist()])

            #distance to surface
            df = distance_led(df, led_y, debug)


        # getting acceleration
        df = acc(df, fps, debug) 


        # angle using tail and head
        df = tail_head_angle(df, debug)
        
        # Save to output path to the correct subdirectory path
        output_csv_path = output_path / csv_file.relative_to(csv_path)
        os.makedirs(output_csv_path.parent, exist_ok=True)
        df.to_csv(output_csv_path, index=False)
        print(f"Saved to ./{output_csv_path}")

    print("Done")
    unique_csv = np.unique([i[0] for i in problems_csv])
    print(unique_csv) if debug else None
    print(len(unique_csv), " files with problems")
    print("Saving problems_csv.txt to output_path")

    # replace np.savetxt with file due to deprecation warning

    with open(output_path / "problems_csv.txt", "w") as f:
        for item in problems_csv:
            # take out items from the list and put in new line
            f.write(f'{item} \n')

    # np.savetxt(output_path / "problems_csv.txt", problems_csv, delimiter=",", fmt="%s")

if __name__ == "__main__":
    # Parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv_path", default = "./data/output/subset/", help="the filepath to subset csv files if not ./data/output/subset/")
    parser.add_argument("--LED_csv_path", default = "./data/output/LED_times.csv", help="the filepath to LED csv file if not ./data/output/LED_times.csv")
    parser.add_argument("--output_path", default = "./data/output/mm_analyse", help="the filepath to output csv if not ./data/output/mm_analyse")
    parser.add_argument("--debug", action="store_true", default = False, help="debug mode (default is false)")
    parser.add_argument("--invalid_thresh", default = 0.25, help="the likelihood threshold for invalid frames (default is 0.25)")
    parser.add_argument("--percent_missing", default = 10, help="the threshold for percent missing data to be reported in problems_csv.txt (default is 10%)")
    parser.add_argument("--percent_low_likelihood", default = 15, help="the threshold for percent low likelihood data to be reported (default is 15%)")
    parser.add_argument("--two_sd_thresh", default = 88.44, help="the threshold for 2SD of body part (default is 88.44)")
    parser.add_argument("--led_invalid_thresh", default = 0.1, help="the percentage threshold for invalid frames in LED timing (default is 0.1)")
    parser.add_argument("--led_jitter_thresh", default = 0.15, help="the percentage threshold for jittery frames in LED timing (default is 0.15)")



    args = parser.parse_args()
    csv_path = Path(args.csv_path)
    LED_csv_path = Path(args.LED_csv_path)
    output_path = Path(args.output_path)
    invalid_thresh = args.invalid_thresh
    percent_missing_thresh = args.percent_missing
    percent_low_likelihood_thresh = args.percent_low_likelihood
    sd_threshold = args.two_sd_thresh
    led_absent_thresh = float(args.led_invalid_thresh)
    led_jitter_thresh = float(args.led_jitter_thresh)
    debug = args.debug

    LED_csv = pd.read_csv(LED_csv_path)

    main(csv_path, LED_csv, percent_missing_thresh, percent_low_likelihood_thresh, invalid_thresh, sd_threshold, output_path, debug)