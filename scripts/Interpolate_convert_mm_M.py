import os
import glob
import pandas as pd
import numpy as np
import random
import argparse
from pathlib import Path


def main(csv_file, out_path, debug):
    # Read csv
    df = pd.read_csv(csv_file)

    # Convert to float
    df = df.astype('float')

    # define X and Y columns to apply the different conversion
    x_columns = ['Tail_X','Body1_X','Body2_X', "Body3_X","Head_X"]
    y_columns = ['Tail_Y','Body1_Y','Body2_Y', "Body3_Y","Head_Y"]

    print(df.head(5)) if debug else None

    # TODO: do something with likelihood, and maybe only interpolate specific columns??

    # Interpolate to fix missing data
    df = df.interpolate()

    # Convert to mm
    for column in x_columns:
        df[column] = df[column] * 0.28

    for column in y_columns:
        df[column] = df[column] * -0.304

    # Write to CSV
    os.makedirs(out_path / csv_file.stem[:3], exist_ok=True)
    df.to_csv(out_path / csv_file.stem[:3] / (csv_file.stem + "_INTER_MM.csv"), index=False)
    print(df.head(5)) if debug else None

    print(f"Ran: {csv_file}, saved to {out_path / csv_file.stem[:3]/ (csv_file.stem+'_INTER_MM.csv')}")

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

    # Create output path if not exist
    os.makedirs(output_path, exist_ok=True)

    # Get all csv files
    csv_files = list(csv_path.glob("**/*.csv"))

    # print csv files
    print(len(csv_files), "csv files found")

    # Iterate through all csv files
    for csv_file in csv_files:
        main(csv_file, output_path, debug)

