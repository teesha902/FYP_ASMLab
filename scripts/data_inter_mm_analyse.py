import numpy as np
import pandas as pd
import glob
import os
import argparse
from pathlib import Path
from scripts.dist_vel_acc import dist_vel_acc, distance

from scripts.data_integrity import check_overall, get_invalids, jittery_frames
# from Interpolate_convert_mm_M import convert_mm

def convert_mm(name, df, debug):
    # Convert to float
    # df = df.astype('float')

    # define X and Y columns to apply the different conversion
    x_columns = ["Tail_x", "Body1_x", "Body2_x", "Body3_x", "Head_x"]
    y_columns = ["Tail_y", "Body1_y", "Body2_y", "Body3_y", "Head_y"]

    print(df.head(5)) if debug else None

    # Convert to mm
    df[x_columns] = df[x_columns].astype(float)* 0.28

    df[y_columns] = df[y_columns].astype(float) * -0.304

    print(f"Converted: {name} to mm")
    return df


def main(csv_path, output_path, debug):
    csv_files = list(csv_path.glob("**/*.csv"))

    problems_csv = []

    # print csv files
    print(len(csv_files), "csv files found")
    print(csv_files) if debug else None

    fps = 30
    # Iterate through all csv files
    for csv_file in csv_files:
        # Read csv
        df = pd.read_csv(csv_file, header = None)
        print(csv_file.name)
        df.columns = df.iloc[2] + "_" + df.iloc[3]
        df.drop([0,1,2,3], inplace=True) # remove the model name and row that just said individual
        df.reset_index(drop=True, inplace=True)
        print(df.head(5)) if debug else None
        
        #check overall data integrity
        percent_missing = check_overall(df, 0.5, debug)
        print(f"{percent_missing:.2f}% missing data")
        
        # if percent_missing > 10:
        #     print("Too much missing data, skipping")
        #     problems_csv.append(csv_file.name)
        #     continue
        
        print("checking for invalid frames") if debug else None
        #check for invalid frames
        invalids = get_invalids(df, 0.5, debug)

        print("checking for jittery frames") if debug else None
        #check for jittery frames
        jittery = jittery_frames(df, 0.5, debug)

        # interpolate
        # df.interpolate(axis=1,limit = inter_limit, limit_area = 'inside', inplace=True)

        # Convert to mm
        df = convert_mm(csv_file.name, df, debug)
        print(df.head(5)) if debug else None

        # do further analysis on the data
        df = dist_vel_acc(df, fps, debug)


        # Save to output path
        # df.to_csv(output_path / csv_file.name, index = False, header = False)

if __name__ == "__main__":
    # Parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv_path", default = "./data/output/subset/", help="the filepath to subset csv files if not ./data/output/subset/")
    parser.add_argument("--output_path", default = "./data/output/inter_mm", help="the filepath to output csv if not ./data/output/inter_mm")
    parser.add_argument("--debug", action="store_true", default = False, help="debug mode (default is false)")
    
    args = parser.parse_args()
    csv_path = Path(args.csv_path)
    output_path = Path(args.output_path)
    debug = args.debug

    main(csv_path, output_path, debug)