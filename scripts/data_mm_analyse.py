import numpy as np
import pandas as pd
import glob
import os
import argparse
from pathlib import Path
from scripts.dist_vel_acc import distance_vel, acc

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

        df.columns = df.iloc[2] + "_" + df.iloc[3] # naming the columns as Tail_x, Tail_y, Tail_likelihood, etc.
        df.drop([0,1,2,3], inplace=True) # remove the first 4 rows. Contains model name, individual name, body part and x/y/likelihood
        df.reset_index(drop=True, inplace=True) # resets the row index
        print(df.head(5)) if debug else None
        
        # convert to numeric dtype from str
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
        
        # print("checking for invalid frames") if debug else None
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
            # check for invalid/jittery frames in LED timing
            mask_low_likelihood = df.loc[start_frame:end_frame, likelihood_columns] < invalid_thresh
            mask_absent = df.loc[start_frame:end_frame, likelihood_columns].isnull()
            combined = mask_low_likelihood | mask_absent
            print (combined.head(5)) if debug else None
            mask = combined.sum(axis=1) >= 3 # if more than 2 columns have low likelihood or absent
            print(mask.head(5)) if debug else None
            if len(combined.index[mask].tolist())/(end_frame-start_frame) > 0.2:
                print(f"{csv_file.name} contains > {20}% invalid frames in LED timing")
                problems_csv.append([csv_file.name, "invalid frames", combined.index[mask].tolist()])

            mask_jitter = df.loc[start_frame:end_frame, "jittery"] == 1
            if len(mask_jitter.index[mask_jitter].tolist())/(end_frame - start_frame) > 0.1:
                print(f" >10% Jittery frames in {csv_file.name} during LED timing")
                problems_csv.append([csv_file.name, mask_jitter.index[mask_jitter].tolist(), "jittery during LED"])

        # getting acceleration
        df = acc(df, fps, debug) 
        
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
    np.savetxt(output_path / "problems_csv.txt", problems_csv, delimiter=",", fmt="%s")


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

    args = parser.parse_args()
    csv_path = Path(args.csv_path)
    LED_csv_path = Path(args.LED_csv_path)
    output_path = Path(args.output_path)
    invalid_thresh = args.invalid_thresh
    percent_missing_thresh = args.percent_missing
    percent_low_likelihood_thresh = args.percent_low_likelihood
    sd_threshold = args.two_sd_thresh
    debug = args.debug

    LED_csv = pd.read_csv(LED_csv_path)

    main(csv_path, LED_csv, percent_missing_thresh, percent_low_likelihood_thresh, invalid_thresh, sd_threshold, output_path, debug)