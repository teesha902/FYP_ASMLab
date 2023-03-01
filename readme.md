# killifish tracking python scripts

## TODO:

- [X] find and stabilize package and python versions, upgrade if neccessary (created requirements.txt)
- [ ] streamline / refactor
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
- [ ] saveable visualisations
- [ ] trajectory angle ? (maybe direction of movement is useful, we only have direction of head to tail rn)
- [ ] integrity column instead of missing/jitter/low thresh coz hard to find every time...

#### stage 2?

- [ ] multiprocessing to improve performance
- [ ] python file for DLC (POC for refine tracklets done)
- [ ] imrpove dynamic threshold?
- [ ] improve jitter detection?

### metrics

1. [X] fish angle (head to tail)
2. [X] dist (cumulative), vel, acc averaged over LED timing --> histogram
3. [ ] surface (needs to incorporate LED coords)
4. [ ] count of frames where y is higher than y_start --> % of frames where fish is above starting --> plot??
5. [ ] averaged angle of movement across frames

# Additions

**main.ipynb** - main jupyter notebook to run everything. Use this to interact with the entire repository.

**LED_times.py** - Script for running LED analysis. Contains video processing, mask creation, clustering analysis and re-analysis of problematic videos. More info available in the readme in scripts folder, and in the script itself.

**data_mm_analyse.py** - Script for running data integrity checks like null/low likelihood and jittery frames, converting pixels to mm, and running the instantaneous analysis such as calculating distance travelled, speed and acceleration.

**data_integrity.py** - Contains code used by `data_mm_analyse.py` for data integrity checks, mainly for checking overall missing data, and calculating jittery frames.

**dist_vel_acc.py** - Contains code used by `data_mm_analyse.py` for converting mm to distance travelled, speed and acceleration per frame respectively.

**SUBSET_CSV_M.py** - script for creating MANUAL subsets. Contains subset parsing and creating individual csvs for each subset for each original DLC csv. Input is DLC csvs path, output path, and the subsets needed. Subsets are given as "[(-6, -3)...(-3, 'start'), ('start','end'), ('end', 3)....(4,6)]", in which 'start' and 'end' denote LED event. Currently, only the first led event in the video is used. Subsets can be designed completely arbitrarily by the user.

## New folder structure

```
ASM_Killifish_repo/
└── data/
│   └── output/
│   │    ├── subset (output from SUBSET_CSV_M.py)
│   │    └── mm_analyse (output from data_mm_analyse.py)
│   ├── csv/ (used to contain DLC output csvs)
│   └── videos/ (original videos)
├── scripts/ (contains the python scripts used)
├── main.ipynb (USE THIS!)
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
