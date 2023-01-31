# Detailed info on scripts

## LED_times.py

LED_times takes in the following arguments:

1. `--video_path <path to videos>` can be used to provide path to a folder containing videos if not in `data/videos`.
2. `--output_path <path to output>` can be used to provide output path for csv if not `data/output`
3. `--debug` flag is used to get debug printouts with default set to false.
4. `--vis` flag is used to visualise background mask, and current mask while LED is detected. This will show up while the video is being processed, great for debugging the mask itself.
5. `--max_led <max number of LED events>` allows to allow for multiple led events. If the folder may contain videos with 2 or more LED events, this can be used. Default is 2.
6. `--no_hist_thresh` allows us to disable dynamic histogram thresholding. It is currently used as histogram threshold is not a mature feature.

This script only runs when run from command line/jupyter notebook. The different functions can be imported to run in other scripts if necessary.

A folder of videos is taken, and each video is processed. The process contains following key steps:

1. creating a background mask using `create_mask()` after 5s of video. The 5s window is to eliminate shake at the start of video due to pressing the shutter/record button.

   The mask creation can have the `sensitive` flag, which is used to define thresholds. For the first run, the brightness threshold (L) is set to 35, and changed to 25 by setting sensitive to true for the second run to re-analyse problematic videos. It converts frame to LAB color format (shown in fig below) and applies a small gaussian blur to decrease noise, before applying a threshold on L for luminance(brightness), and the other 2 channels for filtering the red color (25 to 128 on x-axis, -20 to 40 on the y-axis).

   ![img](https://sensing.konicaminolta.asia/wp-content/uploads/2018/09/3D-LAB.jpg)
2. After background mask, we create a mask for each frame using similar method and thresholds as background subtraction.
3. Background mask is subtracted from frame mask. If we observe more than 2500 non zero pixels after subtraction, that indicates an LED event. Threshold was set using trial and error to avoid noise but see even small LEDs. The timestamp and frame of each frame which meets this threshold is stored in arrays.
4. After we process through the entire video, this array of timestamps is sent to `get_timestamps()` for clustering analysis. This function returns the indexes of timestamps where the first and last timestamps are between 2.5s to 6.5s.
5. We check the output to check how many LED events are observed. If too many events (determined by `max_LED` flag) or no LED events are observed, we store the video name in `problem_vids` dictionary for processing later. Otherwise, timestamps and frame number is appended to `final_timestamps` array and returned.
6. At this point, we re-run this analysis **once** if there are videos with no LED events to check if there are events observed using the lower threshold, using the `sensitive` flag.
7. After the re-analysis is finished, the outputs are saved to output path defined earlier as problem_vids.txt and final timestamps to LED_times.csv .


## data_mm_analyse.py (+ data_integrity.py + dist_vel_acc.py)

data_mm_analyse takes in the following arguments:

1. `--csv_path <path to subset csvs>` can be used to provide path to a folder containing subset csvs if not in `data/output/subset/`.
2. `--output_path <path to output>` can be used to provide output path for csv if not `data/output/mm_analyse`
3. `--invalid_thresh <threshold>` is used to define the likelihood threshold for a frame to be considered invalid. currently set to 0.25
4. `--percent_missing <threshold>` is used to define at what percentage a csv is considered to be problematic and saved to problem_csv.txt along with the output CSV. default is 15%.
5. `--debug` flag is used to get debug printouts with default set to false.

This script incorporates the usage of data_integrity and dist_vel_acc as well. Currently, the script checks an overall level of data missing, and if the missing percentage is higher than the threshold set, it is considered "problematic".

Next, all the invalid frames are marked with a 0 in the likelihood column, allowing for filtering during subset. Furthermore, we check for jitter by creating a histogram of average distance between points on the body of the fish. Using the first empty bin in the histogram after excluding the first few bins, we can set a threshold and find frames where this average distance is higher, possibly indicating jitter.

Now, the pixel coordinates are converted to mm values by multiplying 0.28 for x-axis and -0.304 for y-axis. After this, instantaneous analysis is done to get distance, velocity and acceleration of the fish in that frame. dist_vel_acc.py is used to calculate that.

The output df has the following columns

```
bodyparts_coords,Tail_x,Tail_y,Tail_likelihood,Body1_x,Body1_y,Body1_likelihood,Body2_x,Body2_y,Body2_likelihood,Body3_x,Body3_y,Body3_likelihood,Head_x,Head_y,Head_likelihood,jittery,dist_Tail,dist_Body1,dist_Body2,dist_Body3,dist_Head,Tail_vel,Tail_acc,Body1_vel,Body1_acc,Body2_vel,Body2_acc,Body3_vel,Body3_acc,Head_vel,Head_acc
```

## SUBSET_CSV_M.py

SUBSET_CSV_M takes in the following arguments:

1. `--csv_path <path to DLC csvs>` can be used to provide path to a folder containing DLC csvs if not in `data/csv/`.
2. `--led_path <path to LED_times.csv>` can be used to provid path for LED_times.csv if not `data/output/`
3. `--output_path <path to output>` can be used to provide output path for csv if not `data/output/subset`
4. `--debug` flag is used to get debug printouts with default set to false.
5. `--subset "<subsets list>"` input is **REQUIRED**. This flag defines the _custom_ subsets which are inputted by the user to subset the main DLC csv. This follows the following rules
   * The general pattern is "[(start_time, end_time) , ...]". An example is "[(-6, -3), (-3, 'start'), ('start', 'end'), ('end', 3)]"
   * Here, 'start' and 'end' refer to starting and ending time of the LED event. A negative integer refers to time before the start of LED, and a positive integer refers to time after LED event is finished.
   * It must always be a a tuple () containing 2 values inside a list [], which is passed as a string "" to the argument. This is crucial to it being interpreted correctly.

Currently, only the first led event is used. Furthermore, output saving is done by `output_path/<animal number>/<animal number>_<day>_<subset number>` .

The columns are set as shown below. (OUTDATED)

```
    columns = ["Frames","Tail_X","Tail_Y",'Tail_L',
                'Body1_X','Body1_Y','Body1_L',
                'Body2_X','Body2_Y','Body2_L',
                'Body3_X','Body3_Y','Body3_L',
                'Head_X','Head_Y','Head_L']
```
