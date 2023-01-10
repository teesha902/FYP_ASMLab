"""
The if name == main runs the script when called from command line. This part calls all the other functions.
This is used so that we can import the script without running it. 

Parser is used to take in arguments from command line.
--vis flag is used to visualise background mask, and current mask while LED is detected. 
--video_path can be used to provide path to a folder containing videos if not in data/videos. 
--output_path can be used to provide output path for csv if not data/output
--vis allows us to observe the background and the subtracted mask (default is false). 
--max_led allows to allow for multiple led events. If the folder may contain videos with 2 or more LED 
events, this can be used. Default is 2.

create_mask() creates a mask given the image/frame. It converts frame to LAB color format and applies a 
small gaussian blur to decrease noise, before applying a threshold on L for luminance(brightness), and 
the other 2 channels for filtering the red color. 
Sensitive variable is used to reduce threshold of brightness. This is necessary as we need to filter out
 the higher brightness videos first by using a higher threshold (35) first, and then run the remaining 
 videos where no led was observed through the reduced brightness threshold(25).

get_timestamps() takes in a list of timestamps and returns a list of timestamps where the LED is observed.
It uses clustering to find the start and end of LED observation. the cluster limits are 2.5s to 6s.
If the time difference between 2 timestamps is more than 6s, it is considered as a new observation.

In the main() function, we use video path to find all video files. LED_times array saves the final result 
for each video before saving that data in a csv. The for loop is the main code. for each video, a progress bar
is initiated. A capture object is opened to process each frame using opencv. 

bg flag tracks if a background mask has been created or not, which is done on the frame after **5s**. 
This is done to eliminate effect of shaking at the start of the videos. the small bg if loop stores 
the background mask in bg_mask variable and then turns flag to false.

Next, we go through all the frames wherein a mask for the frame is created, after which we subtract 
background mask from the current frame's mask. we store all the timestamps at which LED is observed.
Next, cluster analysis is used to find the start and end time for the LED event. If no led event or 
more than max_led events are observed, the error is printed and the video is appended to problem_vids, 
otherwise the timings are added to LED_times. 

For the videos from problem videos with no LED event, we re-analyse with a lower "sensitive" threshold
to check if detection works. The videos with problems are printed and saved to problem_vids.txt 
and the LED_times is saved to LED_times.csv to the out_path, by default the data/output folder.

Created by: Aritejh
"""

import numpy as np
import argparse
import cv2
from pathlib import Path
from tqdm import tqdm
import json

def create_mask(frame, sensitive):
    frame_LAB = cv2.cvtColor(cv2.GaussianBlur(frame,(5,5),0), cv2.COLOR_BGR2Lab)
    lower_threshold = (35*2.55, 25+128, -20+128) if not sensitive else (25*2.55, 25+128, -20+128) # changed from 27 to 35 as brightly lit videos were too sensitive
    upper_threshold = (100*2.55, 128+128, 40+128)
    mask = cv2.inRange(frame_LAB, lower_threshold, upper_threshold)
    # print(f'sensitive analysis, lower threshold set to {lower_threshold}') if sensitive else None 
    return mask

def get_timestamps(timestamps, debug):
    final_timestamps = []
    time_difference = 0
    for i, timestamp in enumerate(timestamps):
        if i == 0:
            first_timestamp = i
            last_timestamp = i
            time_difference = 0
        else:
            time_difference += timestamp - timestamps[i - 1]
            # print(f"time difference is {time_difference}") if debug else None

            if 2500 < time_difference < 6500:
                last_timestamp = i
                # print(f"replacing last timestamp to {timestamps[i]}") if debug else None

            elif time_difference >= 6500:
                if last_timestamp > first_timestamp:
                    print(f"replacing first timestamp with {timestamps[i]}, appending {timestamps[first_timestamp], timestamps[last_timestamp]}") if debug else None
                    final_timestamps.append([first_timestamp, last_timestamp])
                first_timestamp = i
                time_difference = 0
    
    if 2500 < time_difference < 6500 and [first_timestamp, last_timestamp] not in final_timestamps:
        final_timestamps.append([first_timestamp, last_timestamp])
        print(f"appending final timestamps {first_timestamp, last_timestamp}") if debug else None
    return final_timestamps

def process_video(video_path, vis, debug, max_LED, LED_times, problem_vids, sensitive = False):
    video = cv2.VideoCapture(str(video_path))
    print(video_path.name)
        
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    progress_bar = tqdm(total=total_frames)
        
    time_for_video=[]
    frame_for_video=[]
    bg = True
    mask_bg = []
        
    # Read until video is completed
    while(video.isOpened()):
        # Capture frame-by-frame
        ret, frame = video.read()

        if bg == True and video.get(cv2.CAP_PROP_POS_MSEC) > 5000:
            mask_bg = create_mask(frame, sensitive)
            bg = False
            print("\n bg created") if debug else None
            if vis == True: 
                cv2.imshow(f'{video_path.name} bg',mask_bg)
        if ret == True and bg == False:  
            # Press Q on keyboard to  exit, for visualization
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
                
            mask_frame = create_mask(frame, sensitive)
            mask_bw = mask_frame - mask_bg
                #find number of non-zero pixels and print timestamp and pixels count if nonzero pixels > 2500
            if np.count_nonzero(mask_bw) > 2500:
                time_for_video.append(video.get(cv2.CAP_PROP_POS_MSEC))
                frame_for_video.append(video.get(cv2.CAP_PROP_POS_FRAMES))
                    # print timestamp of video frame for debugging
                    # print(min(time_for_video), max(time_for_video), min(frame_for_video), max(frame_for_video)) if debug else None
                    # EXPERIMENT IF ERODE AND DILATE IS NEEDED
                if vis == True:  
                    mask_dilate = cv2.dilate(mask_bw, None, iterations=3)
                    mask_erode = cv2.erode(mask_dilate, None, iterations=4)
                    cv2.imshow(f'{video_path.name} mask',mask_erode)
                # Break the loop
        elif ret == False: 
            break
        progress_bar.update(1)

        
        # When everything done, release the video capture object, progress bar, and close frames
    video.release()
    progress_bar.close()
    cv2.destroyAllWindows()
        
    #cluster analysis to find the start index and end index of LED
    print(time_for_video) if debug else None
    final_timestamps = get_timestamps(time_for_video, debug)
    print(final_timestamps) if debug else None

        # output verification
    if len(time_for_video) == 0 or len(final_timestamps) == 0 :
        problem_vids['LED not observed'].append(video_path.name) if video_path.name not in problem_vids['LED not observed'] else None
        print(f"LED not observed in {video_path.name}")
        return False
    elif len(final_timestamps) > max_LED:
        problem_vids['Too many LED events'].append(video_path.name)
        print(f"Too many LED events in {video_path.name}")
        # appends the LED times to the list
        return False
    else:
        for i in final_timestamps:
            LED_times.append([str(video_path.name), f"{time_for_video[i[0]]/1000:.2f}", f"{time_for_video[i[1]]/1000:.2f}", frame_for_video[i[0]], frame_for_video[i[1]]]) 
            print(LED_times[-1])
        return True


def main(video_path, vis, debug, max_LED):
    # Creating the list of videos and initialising arrays
    vid_list = list(video_path.glob("*.mp4"))
    print(f' total videos found are {len(vid_list)}')
    print(f' Videos to be processed are {[i.name for i in vid_list]}') if debug else None
    LED_times = [["name", "start time(s)", "end time(s)", "start frame", "end frame"]]

    problem_vids = {'Too many LED events': [], 'LED not observed': []}
    
    #Looping over videos
    for video_path in vid_list:
        process_video(video_path, vis, debug, max_LED, LED_times, problem_vids)
    return problem_vids, LED_times

if __name__ == "__main__":
    # Parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--video_path", default = "./data/videos/", help="the filepath to video files if not default")
    parser.add_argument("--output_path", default = "./data/output/", help="the filepath to output csv if not default")
    parser.add_argument("--debug", action="store_true", default = False, help="debug mode (default is false)")
    parser.add_argument("--vis", action="store_true", default = False, help="visualise (default is false)")
    parser.add_argument("--max_led", default = 2, help="max number of LED events allowed (default is 2)")

    args = parser.parse_args()
    video_path = Path(args.video_path) 
    out_path = Path(args.output_path) 
    vis = args.vis
    debug = args.debug
    max_LED = args.max_led

    #main process
    problem_vids, LED_times = main(video_path, vis, debug, max_LED)
    # output verification and error handling
    if sum(len(x) for x in problem_vids.values())  > 0:
        print("trigger") if debug else None
        print(f'problems found in {problem_vids}')
        re_analyse = [i for i in problem_vids['LED not observed']]
        for i in re_analyse:
            print(f'running reduced threshold analysis for {i}')
            attempt = process_video(Path(video_path / i), vis, debug, max_LED, LED_times, problem_vids, sensitive = True)
            if attempt == False:
                print(f'failed to process {i}')
            else:
                print(f'successfully processed {i}')
                problem_vids['LED not observed'].remove(i)
        print(f'problems found in {problem_vids}, after running reduced threshold analysis')
    
    # saving to csv        
    csv_path = Path(out_path, "LED_times.csv")
    problem_vids_path = Path(out_path, "problem_vids.txt")
    print(f'saving to {csv_path}')
    np.savetxt(csv_path, LED_times, delimiter=',', fmt = "%s" )
    # save problem vids to out_path/problem_vids.txt
    with open(problem_vids_path, 'w') as fp:
        fp.write(json.dumps(problem_vids))