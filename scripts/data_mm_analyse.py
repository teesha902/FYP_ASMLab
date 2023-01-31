import numpy as np
import pandas as pd
import glob
import os
import argparse
from pathlib import Path
from scripts.dist_vel_acc import dist_vel_acc, distance

from scripts.data_integrity import check_overall, jittery_frames

def convert_mm(name, df, debug):
    # define X and Y columns to apply the different conversion
    x_columns = ["Tail_x", "Body1_x", "Body2_x", "Body3_x", "Head_x"]
    y_columns = ["Tail_y", "Body1_y", "Body2_y", "Body3_y", "Head_y"]

    print(df.head(5)) if debug else None

    # Convert to mm
    df[x_columns] = df[x_columns].astype(float)* 0.28
    df[y_columns] = df[y_columns].astype(float) * -0.304

    print(f"Converted: {name} to mm")
    return df


def main(csv_path, percent_missing_thresh, invalid_thresh, output_path, debug):
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
        df.columns = df.iloc[2] + "_" + df.iloc[3] # naming the columns as Tail_x, Tail_y, Tail_likelihood, etc.
        df.drop([0,1,2,3], inplace=True) # remove the model name and row that just said individual
        df.reset_index(drop=True, inplace=True) # resets the row index
        print(df.head(5)) if debug else None
        
        #check overall data integrity
        percent_missing = check_overall(df, invalid_thresh, debug)
        print(f"{percent_missing:.2f}% missing data")
        
        if percent_missing > percent_missing_thresh:
            print(f"Too much missing data in {csv_file.name}")
            problems_csv.append((csv_file.name, percent_missing))
        
        print("checking for invalid frames") if debug else None
        #replace <bbodypart>_likelihood with 0 or 1 depending on if it is invalid or not.
        # invalid frames are frames where the likelihood is less than the invalid_thresh or null
        likelihood_columns = [col for col in df.columns if "likelihood" in col]
        df[likelihood_columns] = df[likelihood_columns].apply(lambda x:  x.where(x.astype(float) >= invalid_thresh, 0).fillna(0))
        
        print("checking for jittery frames") if debug else None
        #check for jittery frames
        jittery = jittery_frames(df, debug)
        df["jittery"] = 0 # add a jittery column
        df.loc[jittery, "jittery"] = 1

        # Convert to mm
        df = convert_mm(csv_file.name, df, debug)
        print(df.head(5)) if debug else None

        # do further analysis on the data
        df = dist_vel_acc(df, fps, debug)
        
        print(df.head(5)) if debug else None

        # Save to output path
        os.makedirs(output_path, exist_ok=True)
        df.to_csv(output_path / csv_file.name, index=False)
    np.savetxt(output_path / "problems_csv.txt", problems_csv, delimiter=",", fmt="%s")

if __name__ == "__main__":
    # Parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv_path", default = "./data/output/subset/", help="the filepath to subset csv files if not ./data/output/subset/")
    parser.add_argument("--output_path", default = "./data/output/mm_analyse", help="the filepath to output csv if not ./data/output/mm_analyse")
    parser.add_argument("--debug", action="store_true", default = False, help="debug mode (default is false)")
    parser.add_argument("--invalid_thresh", default = 0.25, help="the threshold for invalid frames (default is 0.25)")
    parser.add_argument("--percent_missing", default = 15, help="the threshold for percent missing data (default is 15%)")

    args = parser.parse_args()
    csv_path = Path(args.csv_path)
    output_path = Path(args.output_path)
    invalid_thresh = args.invalid_thresh
    percent_missing_thresh = args.percent_missing
    debug = args.debug

    main(csv_path, percent_missing_thresh, invalid_thresh, output_path, debug)