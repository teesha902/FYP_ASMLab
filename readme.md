# killifish python scripts

## TODO:
- find and stabilize package and python versions, upgrade if neccessary
- reduce hardcoded file paths, make scripts interoperable between mac and windows (pathlib)
- turn hardcoded variables into passable variables
- reduce number of files generated for the average values (1 row csvs) (descriptive data, orientation/*, surface) (POC testing done, verification + full dataset + proper tqdm left, but can be done with refactoring?)
- build an LED detector (POC done @ led_tracker.ipynb)
- python file for DLC (POC for refine tracklets done)

#### stage 2?
- refactor code
- multiprocessing to improve performance
- use notebook for ease of use. May still continue with the scripts format, but use notebook for interfacing instead of terminal 


## Workflow: 
### video ingestion
Rename videos --> record in data.xlsx --> videos in same folder

Video naming: <killifish age and number><exp day><trial number for the day>

### DeepLabCut
DLC --> model config --> analyse videos (config + files + filetype mp4) --> step 2 tracklets --> step 3 refine tracklets (each video) --> output: 2nd video with tracks + excel containing fish part positions

### Missing Data analysis
Check videos or check excel sheet using 
*	Select all blank cells with =COUNTBLANK()
*	Select all cells which contain data with =COUNTA() function
*	Add both to get the number of cells that are supposed to contain data
*	Divide the number of blank cells by the number of all cells (blank and filled)

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