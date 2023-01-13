# killifish tracking python scripts

## TODO:

- [X] find and stabilize package and python versions, upgrade if neccessary (created requirements.txt)
- [ ] streamline / refactor
  - [ ] reduce hardcoded file paths, make scripts interoperable between mac and windows (pathlib)
  - [ ] turn hardcoded variables into passable variables
  - [ ] reduce number of files generated for the average values (1 row csvs) (descriptive data, orientation/*, surface)
  - [ ] refactor to reduce code length
  - [ ] create a notebook for final implementation for ease for running (main.ipynb)
  - [ ] Create a random SUBSET_CSV also?
  - [ ] missing data analysis/likelihood analysis
- [X] build an LED detector (done LED_times.py)
  - [ ] use histogram to set thethreshold dynamically?
  
#### stage 2?

- [ ] multiprocessing to improve performance
- [ ] python file for DLC (POC for refine tracklets done)

# Additions

**main.ipynb** - main jupyter notebook to run everything. Use this to interact with the entire repository. 

**LED_times.py** - Script for running LED analysis. Contains video processing, mask creation, clustering analysis and re-analysis of problematic videos. More info available in the readme in scripts folder, and in the script itself.

**SUBSET_CSV_M.py** - script for creating MANUAL subsets. Contains subset parsing and creating individual csvs for each subset for each original DLC csv. Input is DLC csvs path, output path, and the subsets needed. Subsets are given as "[(-6, -3)...(-3, 'start'), ('start','end'), ('end', 3)....(4,6)]", in which 'start' and 'end' denote LED event. Currently, only the first led event in the video is used. Subsets can be designed completely arbitrarily by the user. 

**Interpolate_convert_mm_M.py** - just a refactored version of the same script as before. This script loads the subset csv, interpolates for missing values, and converts to mm using the * 0.28 for x-axis and *-0.304 for y-axis. saves the new csv in data/output/inter_mm unless specified otherwise.

## New file structure

```
ASM_Killifish_repo/
└── data/
│   └── output/
│   │    ├── subset (output from SUBSET_CSV_M.py)
│   │    └── inter_mm (output from interpolate_convert_mm_M.py)
│   ├── csv/ (used to contain DLC output csvs)
│   └── videos/ (original videos)
├── scripts/ (contains the python scripts used)
├── main.ipynb (USE THIS!)
├── readme.md (BUT READ THIS FIRST!)
├── requirements.txt (keep track of packages used)
└── .gitignore (hidden)
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
