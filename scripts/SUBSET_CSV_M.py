import numpy as np
import pandas as pd
import os
import glob
from pathlib import Path
import argparse
import ast


def main(f, led, out_path, subset_times, debug):
    # read the csv file
    csv = pd.read_csv(f, skiprows= 4, header=None)
    print(csv.head(5)) if debug else None

    # calculate the frame rate
    frame_per_sec_r = (led[4]-led[3])/(led[2]-led[1])
    print(frame_per_sec_r) if debug else None

    # set columns for the subsetted csv
    columns = ["Frames","Tail_X","Tail_Y",'Tail_L',
                'Body1_X','Body1_Y','Body1_L',
                'Body2_X','Body2_Y','Body2_L',
                'Body3_X','Body3_Y','Body3_L',
                'Head_X','Head_Y','Head_L']


    for i, subset_time in enumerate(subset_times):

        # calculate start and end frames
        start_frame =  int(subset_time[0] * frame_per_sec_r) + 1
        end_frame = int(subset_time[1] * frame_per_sec_r) + 1
        print(start_frame, end_frame) if debug else None

        # slice dataframe and set columns
        subset_df = pd.DataFrame(csv.iloc[start_frame:end_frame,:])
        subset_df.columns = columns
        print(subset_df.head(5)) if debug else None
        
        # save to csv: format is out_path/<animal id>/<animal id and day>_<subset number>.csv
        os.makedirs(out_path / f.stem[:3], exist_ok=True)
        subset_df.to_csv(out_path / f.stem[:3]/ (f.stem+f"_{i}.csv"), index=False)
        print(f"Ran: {f}, saved to {out_path / f.stem[:3]/ (f.stem+f'_{i}.csv')}")

def subset_parser(led, subsets):
    subsets_timed = []
    led_start, led_end = led[1], led[2]

    for subset in subsets:
        # subset = (-6,-3)
        subset_parsed = []
        for index, time in enumerate(subset):
            if type(time) == int:
                if time < 0:
                    subset_parsed.insert(index, led_start + time) # this is + because i itself is negative
                else:
                    #i > 0
                    subset_parsed.insert(index,led_end + time)
            else:
                # i is a string
                if time == "start":
                    subset_parsed.insert(index,led_start)
                elif time == "end":
                    subset_parsed.insert(index,led_end)
                else: 
                    raise ValueError("Invalid subset value")
        subsets_timed.append(subset_parsed)
    return subsets_timed


if __name__ == "__main__":
    # Parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv_path", default = "./data/csv/", help="the filepath to csv files if not default")
    parser.add_argument("--led_path", default = "./data/output/LED_times.csv", help="the filepath to LED files if not default")
    parser.add_argument("--output_path", default = "./data/output/subset", help="the filepath to output csv if not default")
    parser.add_argument("--debug", action="store_true", default = False, help="debug mode (default is false)")
    parser.add_argument("--subsets", required= True, help = "subsets to divide the data into. Use [(-6, -3), (-3, 'start'), ('start', 'end'), ('end', 3)].")

    args = parser.parse_args()
    csv_path = Path(args.csv_path) 
    led_path = Path(args.led_path)
    out_path = Path(args.output_path) 
    debug = args.debug
    subsets = ast.literal_eval(args.subsets)
    led_csv = pd.read_csv(led_path)

    # get all csv files
    csv_files = list(csv_path.glob("**/*.csv"))
    print (f'found csv files: {len(csv_files)}')
    print(csv_files) if debug else None

    problem_files = []

    for f in csv_files:
        # for each csv file, find the corresponding LED time
        led = led_csv.loc[led_csv['name'] == f.with_suffix(".mp4").name].to_numpy()
        print(led) if debug else None

        # if there is a corresponding LED time, run the main function
        if led.size > 0:
            led = led[0] # only using the first LED event for now
            subsets_timed = subset_parser(led, subsets)
            print(subsets_timed) if debug else None
            main(f, led, out_path, subsets_timed, debug)
        else:
            print(f"no LED data for {f}")
            problem_files.append(f.stem)
    
    print(f"Subset CSVs created for {len(list(csv_files)) - len(problem_files)} files")
    print(f"{len(problem_files)} files with no LED data: {problem_files}")