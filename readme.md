# killifish tracking python scripts

This repository contains code to ingest and process data for the killifish project in ASM Lab.

## DLC WORKFLOW: 
The package consists of 10 python scripts. The scripts should be run in order, but can also function
independently on the needs of the user. For example, if the user wants to run a full analysis then they
should follow the pipeline below, but if the user only wants to get specific information ( e.g surface
calculations) they can just run the relevant script.

**PIPELINE**:

**PREPARE CSV FILES**
  1. The first step after obtaining CSV files of XY coordinates from Deeplabcut is to rename the files. Deeplabcut adds a large suffix to the end of each CSV file created (e.g DLC_resnet50_KF_Full...le1_50000_el_filtered.csv).
  
  To avoid issues caused by too long file names remove the added suffix: change _d48_23_F1_FDLC_resnet50_KF_Full...le1_50000_el_filtered.csv_ to _d48_23_F1.csv_
    
  2. Once the files have been renamed create the following folder hierarchy:
    - First created a folder called Raw_CSVs.
    - Within the Raw_CSVs folder create a folder titled the name of the batch you want to
      analyse (e.g d48) and place all the raw CSV files containing the XY coordinates inside.
    - Within the batch folder create a folder called Cropped_CSV.
        - The Cropped_CSV folder is where the output of SUBSET_CSV.py and
            Interpolate_convert_mm.py will be written.


**PRE-PROCESS FILES**
1. The first script in the package is SUBSET_CSV.py.
  - The script reads all the raw CSV files in the batch folder (e.g in the d48 folder. Adjust
    input and output path locations to specify the correct location to read in and write
    output files. The script creates 12-second subsets and 6 randomly selected 3-second
    segments within the first minute. The 12-second subsets comprise XY coordinate data
    6 seconds before (-6 to 0 s) and after (0 to 6s) the LED light turns on. The 6
    randomly generated 3-second segments act as a baseline for further analyses. The
    generated 3 seconds serve as a baseline for further analysis.
  - The script produces 2 CSV files for each raw CSV file read in:
    - filename_12s.csv ( for the subsetted 12-second segments)
    - filname_3s.csv (for the 6 randomly selected 3-second segments)
    c. The script writes the outputted files to the Cropped_CSV folder
2. The second script to be run is Interpolate_convert_mm.py
  - The script reads in the subsetted CSV files produced by SUBSET_CSV.py (line ***)
    as well as the raw CSV files (line ***)
  - The script interpolates any missing data in the CSV files using linear interpolation.
    The script also converts the XY data from pixels to mm.
  - The script produces three CSV files:
    - filename_Raw_INTER_MM.csv (CSV file containing interpolated and
      converter to mm XY coordinates of the raw CSV file)
    - Filesname_3S_INTER_MM.csv (CSV file containing interpolated and
      converter to mm XY coordinates of filname_3s.csv file)
    - Filesname_12S_INTER_MM.csv (CSV file containing interpolated and
      converter to mm XY coordinates of filname_12s.csv file)

** The INTER_MM.csv - files are used for the rest of the analysis


**ANALYSIS**

The analysis files can be run in any order, except for the polar plots scripts which require the
orientation scripts to be run first. Each of the analysis scripts reads in all the files in a specified folder.

- Dist_Ac_Vel.py
  - Calculate distance, velocity &amp; acceleration &amp; corrects for incorrect distances (if
    distance is mean +2SD the script using linear interpolation to recalculate distance)
  - outputs per frame metrics and averages
- Trajectory_Plot.py
  - Plots Trajectory line plots for specified files
- Surface.py
  - Calculates the distance between fish and the surface of the tank using different
  parameters
  - Uses max y coordinate reached by fish (head)
  - calculate displacement between max Y and head Y values at:
    - 0S
    - 3S
    - 6S
- Orientation
  - Full_Body_Orientaion.py
    - Calculates median body orientation for 0-3S
    - Body orientation is calculated using the head and tail XY coordinates to
    calculate the angle from tail to head for each frame
  - Head_Orientation_Rand_3_sec.py
    - Calculates mean body orientation for each of the randomly generated 3
    second segments
  - Swimming_Trajectory_Orientaion.py
    - Calculate swimming trajectory ie angle in degrees from head coordinates at
    0s to head coordinates at 3s
- Polar_Plot_Coordinates.py
  - Calculates angle of fish’s trajectory, centred at 0,0.
  - Plots polar plots of angles and stores angles in excel file.
  - Angles are binned into 16 bins
- Dot_Plot.py
  - dot plot shows first and last coordinates of each fish


## TODO:

- [X] find and stabilize package and python versions, upgrade if neccessary (created requirements.txt)
- [X] streamline / refactor
  - [X] reduce hardcoded file paths, make scripts interoperable between mac and windows (pathlib)
  - [X] turn hardcoded variables into passable variables
  - [X] reduce number of files generated for the average values (1 row csvs) (descriptive data, orientation/*, surface)
  - [X] refactor to reduce code length
  - [X] create a notebook for final implementation for ease for running (main.ipynb)
  - [X] Create a random SUBSET_CSV also? done with getting the subsets
  - [X] missing data analysis/likelihood analysis - done in data_integrity.py
  - [X] Save according to the subfolder it was found in
- [X] build an LED detector (done LED_times.py)
  - [X] use histogram to set thethreshold dynamically? tried but does not work as well, will look at it again in stage 2.
- [X] Use interpolate convert before Subset + do data analysis for better interpolation and data rejection? - using interpolate with subset only if needed, current implementation does data integrity analysis + instantaneous analysis before subset.
- [X] weighted average for distance
- [X] separate missing and low likelihood for considering a csv "problematic"
- [X] check if missing/low likelihood is during LED timing
- [ ] verify conda setup and kernel/env setup using pure jupyterlab
- [ ] find sd of fish length for jitter check
- [X] convert angle to 360 degs
- [X] histogram + polar histogram
- [X] find LED coordinate to figure out whether fish is facing led. Also useful for surface.
- [X] saveable visualisations
- [X] trajectory angle ? (maybe direction of movement is useful, we only have direction of head to tail rn) (implemented as angle of max y frame position vs initial)
- [ ] integrity column instead of missing/jitter/low thresh coz hard to find every time...
- [ ] check csv names and videos for led - names and number should be same.
- [X] np.savetxt deprecation fix
- [ ] organizing stuff into folders automation
- [ ] clean up visualisation.py and notebooks. Create a backend graphing function?
- [ ] the dabest test csv bug

### stage 2?

- [ ] multiprocessing to improve performance
- [ ] python file for DLC (POC for refine tracklets done)
- [ ] imrpove dynamic threshold?
- [ ] improve jitter detection?

### metrics

1. [X] fish angle (head to tail)
2. [X] dist (cumulative), vel, acc averaged over LED timing --> histogram
3. [X] surface (needs to incorporate LED coords) (now called distance_led)
4. [X] count of frames where y is higher than y_start --> % of frames where fish is above starting --> plot?? (y_up in the visualisation nb)
5. [ ] averaged angle of movement across frames
6. [X] multiple random before LED dfs --> x different population plots --> add plots to make a "superplot" to compare against LED
7. [X] create trajectory + start from led + ymag + y_up plot
8. [X] Change trajectory polar to trajectory vs distance from LED at start (closer to led is lower)
9. [ ] change colorbar to reflect actual colors

## Files

**main.ipynb** - main jupyter notebook to run LED times and post-DLC analysis.

**scripts/LED_times.py** - Script for running LED analysis. Contains video processing, mask creation, clustering analysis and re-analysis of problematic videos. More info available in the readme in scripts folder, and in the script itself.

**scripts/data_mm_analyse.py** - Script for running data integrity checks like null/low likelihood and jittery frames, converting pixels to mm, and running the instantaneous analysis such as calculating distance travelled, speed and acceleration etc.

**scripts/data_integrity.py** - Contains code used by `data_mm_analyse.py` for data integrity checks, mainly for checking overall missing data, and calculating jittery frames.

**scripts/dist_vel_acc.py** - Contains code used by `data_mm_analyse.py` for converting mm to distance travelled, speed and acceleration per frame respectively.


## Visualisations

Several visualisations are created by `visualisation_<exp set>.ipynb` notebooks. These notebooks are used to create visualisations for the data, and are not used for data processing. The visualisations are saved in the `data/visualisation/<exp set>/` folder. 

To create visualisations for a new set of data, copy the template notebook and rename it. Then, define the experiment name and the paths, and run the cells.

First, a LED df and a pre-LED df are created. This is done to benchmark the animal against itself, and is used in dabest plots later. CSVs with no LED time are skipped. For the non-LED df, a subset of same duration as LED time but occuring before it with decent data quality is chosen. If multiple valid subsets exist, a random subset is chosen.

After creating the dataframes, the visualisations are created.
Currently, the following visualisations are created:


## New folder structure

```
ASM_Killifish_repo/
└── data/
│   └── output/
│   │    ├── <LED analysis output>
|   |    |   ├── LED_times.csv
|   |    |   └── problems_csv.txt 
│   │    └── <Post DLC output CSV>
|   |        ├── uroa/<day>/<fish>
|   |        └── control/<day>/<fish>
│   ├── csv/ (used to contain DLC output csvs)
│   ├── visualisation/ (used to contain plots and csv from visualisation)
|   |   └── <Experiment Set>/<data type>
│   └── videos/<uroa or control>/<fish> (original videos to be used for LED detection)
├── scripts/ (contains the python scripts used)
├── main.ipynb (USE THIS!)
├── visualisation.ipynb (For creating visualisations)
├── readme.md (BUT READ THIS FIRST!)
├── requirements.txt (keep track of packages used)
└── .gitignore (hidden)
```

## Setup

These commands can be run in the command prompt (windows) or terminal (Mac) to get the setup going.

### Git Clone

To clone a repository, use the `git clone` command followed by the repository URL. For example:

```
git clone https://github.com/mechunderlyingbehavior/killifish.git
```

### Conda Installation

Conda can be installed by following the instructions provided on the [Conda website](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html#).

### Create Conda Environment

To create a new conda environment called "killifish" with Python, use the following command:

```
conda create --name killifish python
```

By default, Python 3 is installed.

### Activate environment

```
conda activate killifish
```

### Install Requirements

To install the packages listed in the `requirements.txt` file, use the following command:

```
cd killifish
pip install -r requirements.txt
```

This command should be run within the conda environment you created (in this example, "killifish"). This should be the case as we activated the environment earlier

### launch jupyterlab

Launch jupyterlab using the command below. This should open up the browser in the jupyterlab environment opened in the folder killifish.

```
jupyterlab
```

### Download and put post-DLC data into `/data/`

This will usually contain DLC pickle files, tracked csv and videos, and raw videos.

### Create the control/uroa csv

In this case, we can just copy paste from the google sheet into a uroa_control.csv in the raw data folder. Usually, this is just a csv to tell the program which animal is in uroa and which is in control.

### Run main.ipynb

This notebook contains:
1. processing the raw folder into `./data/csv` for post-DLC csvs, `./data/videos` for the original videos. This follows the structure of `csv/<uroa or control>/<1/2/3/4 for the day>` based on the day dictionary in the ipynb

After this, the raw folder can be deleted

2. LED analysis on the original videos
3. Calculating instantaneous metrics like speed/angle and such

### Run visualisation.ipynb
Create a copy of visualisation_template.ipynb and rename it to the experiment set. After this, you can run all to get the current plots.

If you observe the error where dabest takes too long and chart has too many points, means the naming is not happening appropriately. This happens when files dont follow the `<experiment set>_<animal number>_<day>.csv`


## Previous Workflow:

More info can be found in basecamp/nbox README.

### video ingestion

Rename videos --> record in data.xlsx --> videos in same folder

Video naming: ``<killifish age and number> <exp day> <trial number for the day>``

### DeepLabCut

DLC --> model config --> analyse videos (config + files + filetype mp4) --> step 2 tracklets --> step 3 refine tracklets (each video) --> output: 2nd video with tracks + excel containing fish part positions

### Missing Data analysis

Check videos or check excel sheet using

* Select all blank cells with =COUNTBLANK()
* Select all cells which contain data with =COUNTA() function
* Add both to get the number of cells that are supposed to contain data
* Divide the number of blank cells by the number of all cells (blank and filled)

Collect missing data rates for videos --> color code and plot heatmap to check distribution

If missing data rate > 10%:

- Check if data exists for necessary parts. LED times can be crucial.
- Check if atleast 2 body parts exist, then interpolate
- If still > 10%, custom labelling may be needed.

### Analysis Code

Subset relevant coords (SUBSET_CSV.py) --> Interpolate and convert coords to mm (interpolate-convert_mm.py) --> get distance, velocity, acceleration, correct n incorrect distances based on mean + 2SD (Dist_Ac_Vel.py)

- subset generates 6 randomly selected 3 second segments within the first minute or 6s each before and after LED
- Distance velocity and acc provide raw outputs per frame and descriptive measures?

### Plot generation

- plot trajectory n overlap plots (Trajectory_Plot.py)
- plot dot plot if needed (Dot_plot.py)
- Max Y and displacement between max and head Y coords (Surface.py)
- angle at 3s mark (Head_Orientation.py)

### Inspiration paper:

https://www.biorxiv.org/content/10.1101/2021.03.30.437790v1.full
