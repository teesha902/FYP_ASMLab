import numpy as np
import pandas as pd
import glob
import os
import argparse
from pathlib import Path

from scripts.data_integrity import check_overall, get_invalids, jittery_frames
# from Interpolate_convert_mm_M import convert_mm

def convert_mm(name, df, debug):
    # Convert to float
    df = df.astype('float')

    # define X and Y columns to apply the different conversion
    x_columns = ['Tail_X','Body1_X','Body2_X', "Body3_X","Head_X"]
    y_columns = ['Tail_Y','Body1_Y','Body2_Y', "Body3_Y","Head_Y"]

    print(df.head(5)) if debug else None

    # Convert to mm
    for column in x_columns:
        df[column] = df[column] * 0.28

    for column in y_columns:
        df[column] = df[column] * -0.304

    print(f"Converted: {name} to mm')")


def main(csv_path, output_path, debug):
    csv_files = list(csv_path.glob("**/*.csv"))

    problems_csv = []

    # print csv files
    print(len(csv_files), "csv files found")
    print(csv_files) if debug else None

    # Iterate through all csv files
    for csv_file in csv_files:
        # Read csv
        df = pd.read_csv(csv_file, header = None)
        print(csv_file.name)
        df.drop([0,1], inplace=True)
        df.reset_index(drop=True, inplace=True)

        print(df.head(5)) if debug else None
        #check overall data integrity
        percent_missing = check_overall(df, 0.5, debug)
        print(f"{percent_missing}% missing data")
        
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
        # convert_mm(csv_file.name, df, debug)


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